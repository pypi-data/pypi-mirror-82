"""New style (fast) tag count annos

Use these for new projects.

"""
from mbf_genomics.annotator import Annotator
import numpy as np
import pypipegraph as ppg
import hashlib
import pandas as pd
from pathlib import Path
from dppd import dppd
import dppd_plotnine  # noqa:F401
from mbf_qualitycontrol import register_qc, QCCollectingJob, qc_disabled
from mbf_genomics.util import parse_a_or_c_to_plot_name

dp, X = dppd()


# ## Base classes and strategies - skip these if you just care about using TagCount annotators
class _CounterStrategyBase:
    cores_needed = 1

    def extract_lookup(self, data):
        """Adapter for count strategies that have different outputs
        (e.g. one-hashmap-unstranded or two-hashmaps-one-forward-one-reversed)
        """
        return data


class CounterStrategyStrandedRust(_CounterStrategyBase):
    cores_needed = -1
    name = "stranded"

    def __init__(self):
        self.disable_sanity_check = False

    def count_reads(
        self, interval_strategy, genome, bam_filename, bam_index_name, reverse=False
    ):
        # bam_filename = bamfil

        intervals = interval_strategy._get_interval_tuples_by_chr(genome)
        gene_intervals = IntervalStrategyGene()._get_interval_tuples_by_chr(genome)
        from mbf_bam import count_reads_stranded

        res = count_reads_stranded(
            bam_filename, bam_index_name, intervals, gene_intervals
        )
        self.sanity_check(res, bam_filename)
        return res

    def sanity_check(self, foward_and_reverse, bam_filename):
        if self.disable_sanity_check:
            return
        error_count = 0
        forward, reverse = foward_and_reverse
        for gene_stable_id, forward_count in forward.items():
            reverse_count = reverse.get(gene_stable_id, 0)
            if (reverse_count > 100) and (reverse_count > forward_count * 1.1):
                error_count += 1
        if error_count > 0.1 * len(forward):
            raise ValueError(
                "Found at least %.2f%% of genes to have a reverse read count (%s) "
                "above 110%% of the exon read count (and at least 100 tags). "
                "This indicates that this lane (%s) should have been reversed before alignment. "
                "Set reverse_reads=True on your Lane object"
                % (
                    100.0 * error_count / len(forward),
                    self.__class__.__name__,
                    bam_filename,
                )
            )

    def extract_lookup(self, data):
        """Adapter for count strategies that have different outputs
        (e.g. one-hashmap-unstranded or two-hashmaps-one-forward-one-reversed)
        """
        return data[0]


class CounterStrategyUnstrandedRust(_CounterStrategyBase):
    cores_needed = -1
    name = "unstranded"

    def count_reads(
        self, interval_strategy, genome, bam_filename, bam_index_name, reverse=False
    ):
        # bam_filename = bamfil

        intervals = interval_strategy._get_interval_tuples_by_chr(genome)
        gene_intervals = IntervalStrategyGene()._get_interval_tuples_by_chr(genome)
        # chr -> [gene_id, strand, [start], [stops]
        from mbf_bam import count_reads_unstranded

        res = count_reads_unstranded(
            bam_filename, bam_index_name, intervals, gene_intervals
        )
        return res


class _IntervalStrategy:
    def get_interval_lengths_by_gene(self, genome):
        by_chr = self._get_interval_tuples_by_chr(genome)
        length_by_gene = {}
        for chr, tups in by_chr.items():
            for tup in tups:  # stable_id, strand, [starts], [stops]
                gene_stable_id = tup[0]
                length = 0
                for start, stop in zip(tup[2], tup[3]):
                    length += stop - start
                length_by_gene[gene_stable_id] = length
        return length_by_gene

    def _get_interval_tuples_by_chr(self, genome):  # pragma: no cover
        raise NotImplementedError()

    def get_deps(self):
        return []


class IntervalStrategyGenomicRegion(_IntervalStrategy):
    """Used internally by _FastTagCounterGR"""

    def __init__(self, gr):
        self.gr = gr
        self.name = f"GR_{gr.name}"

    def _get_interval_tuples_by_chr(self, genome):
        result = {chr: [] for chr in genome.get_chromosome_lengths()}
        if self.gr.genome != genome:  # pragma: no cover
            raise ValueError("Mismatched genomes")
        df = self.gr.df
        if not "strand" in df.columns:
            df = df.assign(strand=1)
        df = df[["chr", "start", "stop", "strand"]]
        if df.index.duplicated().any():
            raise ValueError("index must be unique")
        for tup in df.itertuples():
            result[tup.chr].append((str(tup[0]), tup.strand, [tup.start], [tup.stop]))
        return result


class IntervalStrategyGene(_IntervalStrategy):
    """Count from TSS to TES"""

    name = "gene"

    def _get_interval_tuples_by_chr(self, genome):
        result = {chr: [] for chr in genome.get_chromosome_lengths()}
        gene_info = genome.df_genes
        for tup in gene_info[["chr", "start", "stop", "strand"]].itertuples():
            result[tup.chr].append((tup[0], tup.strand, [tup.start], [tup.stop]))
        return result


class IntervalStrategyExon(_IntervalStrategy):
    """count all exons"""

    name = "exon"

    def _get_interval_tuples_by_chr(self, genome):
        result = {chr: [] for chr in genome.get_chromosome_lengths()}
        for gene in genome.genes.values():
            exons = gene.exons_merged
            result[gene.chr].append(
                (gene.gene_stable_id, gene.strand, list(exons[0]), list(exons[1]))
            )
        return result


class IntervalStrategyIntron(_IntervalStrategy):
    """count all introns"""

    name = "intron"

    def _get_interval_tuples_by_chr(self, genome):
        result = {chr: [] for chr in genome.get_chromosome_lengths()}
        for gene in genome.genes.values():
            exons = gene.introns_strict
            result[gene.chr].append(
                (gene.gene_stable_id, gene.strand, list(exons[0]), list(exons[1]))
            )
        return result


class IntervalStrategyExonSmart(_IntervalStrategy):
    """For protein coding genes: count only in exons of protein-coding transcripts.
    For other genes: count all exons"""

    name = "exonsmart"

    def _get_interval_tuples_by_chr(self, genome):
        result = {chr: [] for chr in genome.get_chromosome_lengths()}
        for g in genome.genes.values():
            e = g.exons_protein_coding_merged
            if len(e[0]) == 0:
                e = g.exons_merged
            result[g.chr].append((g.gene_stable_id, g.strand, list(e[0]), list(e[1])))
        return result


# Now the actual tag count annotators
class TagCountCommonQC:
    def register_qc(self, genes):
        if not qc_disabled():
            self.register_qc_distribution(genes)
            self.register_qc_pca(genes)
            # self.register_qc_cummulative(genes)

    def register_qc_distribution(self, genes):
        output_filename = genes.result_dir / self.qc_folder / "read_distribution.png"
        output_filename.parent.mkdir(exist_ok=True)

        def plot(output_filename, elements):
            df = genes.df
            df = dp(df).select({x.aligned_lane.name: x.columns[0] for x in elements}).pd
            if len(df) == 0:
                df = pd.DataFrame({"x": [0], "y": [0], "text": "no data"})
                dp(df).p9().add_text("x", "y", "text").render(output_filename).pd
            else:
                plot_df = dp(df).melt(var_name="sample", value_name="count").pd

                plot = dp(plot_df).p9().theme_bw()
                print(df)

                if ((df > 0).sum(axis=0) > 1).any() and len(df) > 1:
                    plot = plot.geom_violin(
                        dp.aes(x="sample", y="count"), width=0.5, bw=0.1
                    )
                if len(plot_df["sample"].unique()) > 1:
                    plot = plot.annotation_stripes(fill_range=True)
                if (plot_df["count"] > 0).any():
                    # can't have a log boxplot with all nans (log(0))
                    plot = plot.scale_y_continuous(
                        trans="log10",
                        name=self.qc_distribution_scale_y_name,
                        breaks=[1, 10, 100, 1000, 10000, 100_000, 1e6, 1e7],
                    )
                print(plot_df)

                return (
                    plot.add_boxplot(
                        x="sample", y="count", _width=0.1, _fill=None, _color="blue"
                    )
                    .turn_x_axis_labels()
                    .title("Raw read distribution")
                    .hide_x_axis_title()
                    .render_args(limitsize=False)
                    .render(output_filename, width=0.2 * len(elements) + 1, height=4)
                )

        return register_qc(
            QCCollectingJob(output_filename, plot)
            .depends_on(genes.add_annotator(self))
            .add(self)
        )

    def register_qc_pca(self, genes):
        output_filename = genes.result_dir / self.qc_folder / "pca.png"

        def plot(output_filename, elements):
            import sklearn.decomposition as decom

            if len(elements) == 1:
                xy = np.array([[0], [0]]).transpose()
                title = "PCA %s - fake / single sample" % genes.name
            else:
                pca = decom.PCA(n_components=2, whiten=False)
                data = genes.df[[x.columns[0] for x in elements]]
                data -= data.min()  # min max scaling 0..1
                data /= data.max()
                data = data[~pd.isnull(data).any(axis=1)]  # can' do pca on NAN values
                if len(data):
                    pca.fit(data.T)
                    xy = pca.transform(data.T)
                    title = "PCA %s\nExplained variance: x %.2f%%, y %.2f%%" % (
                        genes.name,
                        pca.explained_variance_ratio_[0] * 100,
                        pca.explained_variance_ratio_[1] * 100,
                    )
                else:
                    xy = np.array(
                        [[0] * len(elements), [0] * len(elements)]
                    ).transpose()
                    title = "PCA %s - fake / no rows" % genes.name

            plot_df = pd.DataFrame(
                {"x": xy[:, 0], "y": xy[:, 1], "label": [x.plot_name for x in elements]}
            )
            print(plot_df)
            (
                dp(plot_df)
                .p9()
                .theme_bw()
                .add_scatter("x", "y")
                .add_text(
                    "x",
                    "y",
                    "label",
                    # cool, this can go into an endless loop...
                    # _adjust_text={
                    # "expand_points": (2, 2),
                    # "arrowprops": {"arrowstyle": "->", "color": "red"},
                    # },
                )
                .scale_color_many_categories()
                .title(title)
                .render(output_filename, width=8, height=6)
            )

        return register_qc(
            QCCollectingJob(output_filename, plot)
            .depends_on(genes.add_annotator(self))
            .add(self)
        )


class _FastTagCounter(Annotator, TagCountCommonQC):
    def __init__(
        self, aligned_lane, count_strategy, interval_strategy, column_name, column_desc
    ):
        if not hasattr(aligned_lane, "get_bam"):
            raise ValueError("_FastTagCounter only accepts aligned lanes!")
        self.aligned_lane = aligned_lane
        self.genome = self.aligned_lane.genome
        self.count_strategy = count_strategy
        self.interval_strategy = interval_strategy
        self.columns = [(column_name % (self.aligned_lane.name,)).strip()]
        self.cache_name = (
            "FT_%s_%s" % (count_strategy.name, interval_strategy.name)
            + "_"
            + hashlib.md5(self.columns[0].encode("utf-8")).hexdigest()
        )
        self.column_properties = {self.columns[0]: {"description": column_desc}}
        self.vid = aligned_lane.vid
        self.cores_needed = count_strategy.cores_needed
        self.plot_name = self.aligned_lane.name
        self.qc_folder = f"{self.count_strategy.name}_{self.interval_strategy.name}"
        self.qc_distribution_scale_y_name = "raw counts"

    def calc(self, df):
        if ppg.inside_ppg():
            data = self._data
        else:
            data = self.calc_data()
        lookup = self.count_strategy.extract_lookup(data)
        result = []
        for gene_stable_id in df["gene_stable_id"]:
            result.append(lookup.get(gene_stable_id, 0))
        result = np.array(result, dtype=np.float)
        return pd.Series(result)

    def deps(self, _genes):
        return [self.load_data()]

    def calc_data(self):
        bam_file, bam_index_name = self.aligned_lane.get_bam_names()
        return self.count_strategy.count_reads(
            self.interval_strategy, self.genome, bam_file, bam_index_name
        )

    def load_data(self):
        cf = Path(ppg.util.global_pipegraph.cache_folder) / "FastTagCounters"
        cf.mkdir(exist_ok=True)
        return (
            ppg.CachedAttributeLoadingJob(
                cf / self.cache_name, self, "_data", self.calc_data
            )
            .depends_on(self.aligned_lane.load())
            .use_cores(-1)
        )


class _FastTagCounterGR(Annotator):
    def __init__(self, aligned_lane, count_strategy, column_name, column_desc):
        if not hasattr(aligned_lane, "get_bam"):
            raise ValueError("_FastTagCounter only accepts aligned lanes!")
        self.aligned_lane = aligned_lane
        self.genome = self.aligned_lane.genome
        self.count_strategy = count_strategy
        self.columns = [(column_name % (self.aligned_lane.name,)).strip()]
        self.cache_name = (
            "FT_%s_%s" % (count_strategy.name, "on_gr")
            + "_"
            + hashlib.md5(self.columns[0].encode("utf-8")).hexdigest()
        )
        self.column_properties = {self.columns[0]: {"description": column_desc}}
        self.vid = aligned_lane.vid
        self.cores_needed = count_strategy.cores_needed
        self.plot_name = self.aligned_lane.name
        # self.qc_folder = f"{self.count_strategy.name}_{self.interval_strategy.name}"
        # self.qc_distribution_scale_y_name = "raw counts"

    def calc(self, df):
        if ppg.inside_ppg():
            data = self._data
        else:
            data = self.calc_data()
        lookup = self.count_strategy.extract_lookup(data)
        result = []
        for idx in df.index:
            result.append(lookup.get(str(idx), 0))
        result = np.array(result, dtype=np.float)
        return pd.Series(result)

    def deps(self, gr):
        return [self.load_data(gr)]

    def calc_data(self, gr):
        def inner():
            bam_file, bam_index_name = self.aligned_lane.get_bam_names()
            return self.count_strategy.count_reads(
                IntervalStrategyGenomicRegion(gr), self.genome, bam_file, bam_index_name
            )

        return inner

    def load_data(self, gr):
        cf = gr.cache_dir
        cf.mkdir(exist_ok=True)
        return (
            ppg.CachedAttributeLoadingJob(
                cf / self.cache_name, self, "_data", self.calc_data(gr)
            )
            .depends_on(self.aligned_lane.load())
            .depends_on(gr.load())
            .use_cores(-1)  # should be count_strategy cores needed, no?
        )


#
# ## Raw tag count annos for analysis usage


class ExonSmartStrandedRust(_FastTagCounter):
    def __init__(self, aligned_lane):
        _FastTagCounter.__init__(
            self,
            aligned_lane,
            CounterStrategyStrandedRust(),
            IntervalStrategyExonSmart(),
            "Exon, protein coding, stranded smart tag count %s",
            "Tag count inside exons of protein coding transcripts (all if no protein coding transcripts) exons, correct strand only",
        )


class ExonSmartUnstrandedRust(_FastTagCounter):
    def __init__(self, aligned_lane):
        _FastTagCounter.__init__(
            self,
            aligned_lane,
            CounterStrategyUnstrandedRust(),
            IntervalStrategyExonSmart(),
            "Exon, protein coding, unstranded smart tag count %s",
            "Tag count inside exons of protein coding transcripts (all if no protein coding transcripts)  both strands",
        )


class ExonStrandedRust(_FastTagCounter):
    def __init__(self, aligned_lane):
        _FastTagCounter.__init__(
            self,
            aligned_lane,
            CounterStrategyStrandedRust(),
            IntervalStrategyExon(),
            "Exon, protein coding, stranded tag count %s",
            "Tag count inside exons of protein coding transcripts (all if no protein coding transcripts) exons, correct strand only",
        )


class ExonUnstrandedRust(_FastTagCounter):
    def __init__(self, aligned_lane):
        _FastTagCounter.__init__(
            self,
            aligned_lane,
            CounterStrategyUnstrandedRust(),
            IntervalStrategyExon(),
            "Exon, protein coding, unstranded tag count %s",
            "Tag count inside exons of protein coding transcripts (all if no protein coding transcripts)  both strands",
        )


class GeneStrandedRust(_FastTagCounter):
    def __init__(self, aligned_lane):
        _FastTagCounter.__init__(
            self,
            aligned_lane,
            CounterStrategyStrandedRust(),
            IntervalStrategyGene(),
            "Gene, stranded tag count %s",
            "Tag count inside gene body (tss..tes), correct strand only",
        )


class GeneUnstrandedRust(_FastTagCounter):
    def __init__(self, aligned_lane):
        _FastTagCounter.__init__(
            self,
            aligned_lane,
            CounterStrategyUnstrandedRust(),
            IntervalStrategyGene(),
            "Gene unstranded tag count %s",
            "Tag count inside gene body (tss..tes), both strands",
        )


def GRUnstrandedRust(aligned_lane):
    return _FastTagCounterGR(
        aligned_lane,
        CounterStrategyUnstrandedRust(),
        "Tag count %s",
        "Tag count inside region, both strands",
    )


def GRStrandedRust(aligned_lane):
    return _FastTagCounterGR(
        aligned_lane,
        CounterStrategyStrandedRust(),
        "Tag count %s",
        "Tag count inside region, stranded",
    )


# we are keeping the python ones for now as reference implementations
GeneUnstranded = GeneUnstrandedRust
GeneStranded = GeneStrandedRust
ExonStranded = ExonStrandedRust
ExonUnstranded = ExonUnstrandedRust
ExonSmartStranded = ExonSmartStrandedRust
ExonSmartUnstranded = ExonSmartUnstrandedRust

# ## Normalizing annotators - convert raw tag counts into something normalized


class _NormalizationAnno(Annotator, TagCountCommonQC):
    def __init__(self, base_column_spec):
        from ..util import parse_a_or_c_to_anno, parse_a_or_c_to_column

        self.raw_anno = parse_a_or_c_to_anno(base_column_spec)
        self.raw_column = parse_a_or_c_to_column(base_column_spec)
        if self.raw_anno is not None:
            self.genome = self.raw_anno.genome
            self.vid = getattr(self.raw_anno, "vid", None)
            self.aligned_lane = getattr(self.raw_anno, "aligned_lane", None)
        else:
            self.genome = None
            self.vid = None
            self.aligned_lane = None
        self.columns = [self.raw_column + " " + self.name]
        self.cache_name = (
            self.__class__.__name__
            + "_"
            + hashlib.md5(self.columns[0].encode("utf-8")).hexdigest()
        )
        if self.raw_anno is not None:
            self.plot_name = getattr(self.raw_anno, "plot_name", self.raw_column)
            if hasattr(self.raw_anno, "count_strategy"):
                if hasattr(self.raw_anno, "interval_strategy"):
                    iv_name = self.raw_anno.interval_strategy.name
                else:
                    iv_name = "-"
                self.qc_folder = f"normalized_{self.name}_{self.raw_anno.count_strategy.name}_{iv_name}"
            else:
                self.qc_folder = f"normalized_{self.name}"
        else:
            self.plot_name = parse_a_or_c_to_plot_name(base_column_spec)
            self.qc_folder = f"normalized_{self.name}"
        self.qc_distribution_scale_y_name = self.name

    def dep_annos(self):
        if self.raw_anno is None:
            return []
        else:
            return [self.raw_anno]


class NormalizationCPM(_NormalizationAnno):
    """Normalize to 1e6 by taking the sum of all genes"""

    def __init__(self, base_column_spec):
        self.name = "CPM"
        self.normalize_to = 1e6
        super().__init__(base_column_spec)
        self.column_properties = {
            self.columns[0]: {
                "description": "Tag count inside protein coding (all if no protein coding transcripts) exons, normalized to 1e6 across all genes"
            }
        }

    def calc(self, df):
        raw_counts = df[self.raw_column]
        total = max(1, float(raw_counts.sum()))  # avoid division by 0
        result = raw_counts * (self.normalize_to / total)
        return pd.Series(result)


class NormalizationTPM(_NormalizationAnno):
    """Normalize to transcripts per million, ie.
        count / length * (1e6 / (sum_i(count_/length_i)))

    """

    def __init__(self, base_column_spec, interval_strategy=None):
        self.name = "TPM"
        self.normalize_to = 1e6
        super().__init__(base_column_spec)
        if self.raw_anno is None:  # pragma: no cover
            if interval_strategy is None:  # pragma: no cover
                raise ValueError(
                    "TPM normalization needs to know the intervals used. Either base of a FastTagCount annotator or pass in an interval strategy"
                )
            self.interval_strategy = interval_strategy
        else:
            self.interval_strategy = self.raw_anno.interval_strategy
        self.column_properties = {
            self.columns[0]: {"description": "transcripts per million"}
        }

    def calc(self, df):
        raw_counts = df[self.raw_column]
        length_by_gene = self.interval_strategy.get_interval_lengths_by_gene(
            self.genome
        )
        result = np.zeros(raw_counts.shape, float)
        for ii, gene_stable_id in enumerate(df["gene_stable_id"]):
            result[ii] = raw_counts.iloc[ii] / length_by_gene[gene_stable_id]
        total = float(result[~pd.isnull(result)].sum())
        factor = 1e6 / total
        result = result * factor
        return pd.DataFrame({self.columns[0]: result})


class NormalizationFPKM(Annotator):
    def __init__(self, raw_anno):
        raise NotImplementedError(
            "FPKM is a bad thing to use. It is not supported by mbf"
        )


class Salmon(Annotator):
    """Add salmon gene level estimation calculated on a raw Sample
    """

    def __init__(
        self,
        raw_lane,
        prefix="Salmon",
        options={
            # "--validateMappings": None,  this always get's set by aligners.Salmon
            "--gcBias": None,
            "--seqBias": None,
        },
        libtype="A",
        accepted_biotypes=None,  # set(("protein_coding", "lincRNA")),
        salmon_version="_last_used",
    ):
        self.raw_lane = raw_lane
        self.options = options.copy()
        self.libtype = libtype
        self.accepted_biotypes = accepted_biotypes
        self.salmon_version = salmon_version
        self.columns = [
            f"{prefix} TPM {raw_lane.name}",
            f"{prefix} NumReads {raw_lane.name}",
        ]

    def deps(self, ddf):
        import mbf_externals

        return mbf_externals.aligners.Salmon(
            self.accepted_biotypes, version=self.salmon_version
        ).run_quant_on_raw_lane(
            self.raw_lane, ddf.genome, self.libtype, self.options, gene_level=True
        )

    def calc_ddf(self, ddf):
        quant_path = Path(self.deps(ddf).job_id).parent / "quant.genes.sf"
        in_df = pd.read_csv(quant_path, sep="\t").set_index("Name")[["TPM", "NumReads"]]
        in_df.columns = self.columns
        res = in_df.reindex(ddf.df.gene_stable_id)
        res.index = ddf.df.index
        return res
