import pypipegraph as ppg
import subprocess
import pandas as pd
from pathlib import Path
import abc
import dppd

dp, X = dppd.dppd()
from mbf_qualitycontrol import register_qc, QCCollectingJob


class _PostProcessor(abc.ABC):
    """Postprocess an AlignedSample into a new AlignedSample"""

    @abc.abstractmethod
    def process(self, input_bam_name, output_bam_name, result_dir):
        pass  # pragma: no cover

    def further_jobs(self, new_lane, parent_lane):
        """further jobs beyond the processing - But  not qc, do that in register_qc"""
        pass  # pragma: no cover

    @abc.abstractmethod
    def register_qc(self, new_lane):
        pass  # pragma: no cover

    def get_dependencies(self):
        return [ppg.FunctionInvariant(self.name + "_post_process", self.process)]

    def get_parameters(self):
        return ()

    def get_vid(self, source_vid):  # pragma: no cover
        return source_vid


class SubtractOtherLane(_PostProcessor):
    """Subtract all reads (by name) matching in other_alignment.
    Probably only useful for single end data.
    """

    def __init__(self, other_alignment):
        self.other_alignment = other_alignment
        self.name = "_minus_" + other_alignment.name
        self.result_folder_name = "subtracted"

    def process(self, input_bam_name, output_bam_name, result_dir):
        import mbf_bam

        mbf_bam.subtract_bam(
            str(output_bam_name),
            str(input_bam_name),
            str(self.other_alignment.get_bam_names()[0]),
        )

    def get_dependencies(self):
        import mbf_bam

        return super().get_dependencies() + [
            self.other_alignment.load(),
            ppg.ParameterInvariant(
                "SubtractOtherLane.mbf_bam.version", mbf_bam.__version__
            ),
        ]

    def get_vid(self, source_vid):
        if source_vid == self.other_alignment.vid:
            vid = source_vid
        else:
            vid = [source_vid, "-", self.other_alignment.vid]
        return vid

    def further_jobs(self, new_lane, parent_lane):
        def write_delta(of):
            was = parent_lane.mapped_reads()
            now = new_lane.mapped_reads()
            delta = was - now
            Path(of).write_text(
                f"Subtracted {self.other_alignment.name} from {parent_lane.name}.\nLost {delta} reads of {was} ({delta / was * 100:.2f}%)"
            )

        delta_job = ppg.FileGeneratingJob(
            new_lane.result_dir / "subtract_delta.txt", write_delta
        ).depends_on(new_lane.load())
        return [delta_job]

    def register_qc(self, new_lane):
        """Plot for to see how much you lost.

        """
        output_filename = (
            new_lane.result_dir / ".." / "alignment_substract.png"
        ).resolve()
        print(output_filename)

        def calc_and_plot(output_filename, lanes):
            parts = []
            for lane in lanes:
                was = lane.parent.mapped_reads()
                now = lane.mapped_reads()
                lost = was - now
                parts.append(
                    pd.DataFrame(
                        {
                            "what": ["kept", "lost"],
                            "count": [now, lost],
                            "sample": lane.name,
                        }
                    )
                )
            df = pd.concat(parts)
            return (
                dp(df)
                .categorize("what", ["lost", "kept"])
                .p9()
                .theme_bw()
                .annotation_stripes()
                .add_bar(
                    "sample", "count", fill="what", position="stack", stat="identity"
                )
                .title(lanes[0].genome.name + " substraction")
                .turn_x_axis_labels()
                .scale_y_continuous(labels=lambda xs: ["%.2g" % x for x in xs])
                .render_args(width=len(parts) * 0.2 + 1, height=5)
                .render(output_filename)
            )

        return register_qc(
            QCCollectingJob(output_filename, calc_and_plot)
            .depends_on(new_lane.load())
            .add(new_lane)
        )  # since everybody says self.load, we get them all


class UmiTools_Dedup(_PostProcessor):
    def __init__(self, method="directional"):
        self.method = method
        allowed_methods = (
            "unique",
            "percentile",
            ",cluster",
            "adjacency",
            "directional",
        )
        if method not in allowed_methods:
            raise ValueError(f"Method not in allowed methods '{allowed_methods}'")
        self.name = f"UMI-tools_dedup-{method}"
        self.result_folder_name = self.name

    def process(self, input_bam_name, output_bam_name, result_dir):
        cmd = [
            "umi_tools",
            "dedup",
            "-I",
            str(input_bam_name.absolute().resolve()),
            "-S",
            str(output_bam_name.absolute().resolve()),
            "-L",
            str((result_dir / "umi_tools.log").absolute().resolve()),
            "--output-stats",
            str(result_dir / "umi_tools_stats"),
            "--method",
            self.method,
        ]
        import umi_tools.dedup

        # we are running umitools within the slave process
        # no real need to fork, and
        # I couldn't get them to die on 'interactive abort'...
        umi_tools.dedup.main(cmd)

    def register_qc(self, new_lane):
        pass  # pragma: no cover

    def get_version(self):
        return (
            subprocess.check_output(["umi_tools", "--version"]).decode("utf-8").strip()
        )

    def get_parameters(self):
        return (self.get_version(),)  # method is being taken care of by name


class AnnotateFastqBarcodes(_PostProcessor):
    """Annotate cell and umi barcodes from _R1_ fastq files.
    ala dropseq"""

    def __init__(self, raw_lane, barcodes_to_slices):
        self.name = "AnnotateCellAndUMI"
        self.result_folder_name = self.name
        self.raw_lane = raw_lane
        self.barcodes_to_slices = [
            (x, y[0], y[1]) for (x, y) in barcodes_to_slices.items()
        ]
        for tag, start, end in self.barcodes_to_slices:
            if len(tag) != 2:
                raise ValueError("Tag must be two uppercase characters")
            if tag.upper() != tag:
                raise ValueError("Tag must be two uppercase characters")
                if (type(start) != int) or (type(end) != int):
                    raise ValueError(
                        f"Indices must be exactly 2 integers - was {repr(start)}, {repr(end)}"
                    )
                if start >= end or start < 0 or end < 0:
                    raise ValueError(
                        "Invalid index. Must be (start,end) with start < end. No python slicing."
                    )

    def process(self, input_bam_name, output_bam_name, result_dir):
        fastq2_filenames = [x[0] for x in self.raw_lane.input_strategy()]
        import mbf_bam

        mbf_bam.annotate_barcodes_from_fastq(
            str(output_bam_name),
            str(input_bam_name),
            [str(x) for x in fastq2_filenames],
            self.barcodes_to_slices,
        )

    def register_qc(self, new_lane):
        pass  # pragma: no cover
