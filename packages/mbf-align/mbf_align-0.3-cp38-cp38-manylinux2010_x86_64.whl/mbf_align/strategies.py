from pathlib import Path
import os
import shutil
import requests
import hashlib
import pypipegraph as ppg
from collections.abc import Iterable
from mbf_externals.util import download_file


def build_fastq_strategy(input_strategy):
    """smartly find fastq input files

    Parameters
    ----------
        input_strategy - varied
            FASTQsFrom* object - return the object
            str/Path - file: treat as single fastq(.gz) file
            str/Path - folder: treat as folder
            pypipegraph job: extract filenames
            list - recurvively apply build_fastq_strategy and FASTQsJoin them
        """

    if isinstance(input_strategy, _FASTQsBase):
        return input_strategy
    elif isinstance(input_strategy, str) or isinstance(input_strategy, Path):
        p = Path(input_strategy)
        if p.is_dir():
            input_strategy = FASTQsFromFolder(p)
        else:
            input_strategy = FASTQsFromFile(p)
    elif isinstance(input_strategy, ppg.FileGeneratingJob):
        input_strategy = FASTQsFromJob(input_strategy)
    elif isinstance(input_strategy, Iterable):
        if all((isinstance(x, (str, Path)) for x in input_strategy)):
            input_strategy = FASTQsFromFiles(input_strategy)
        else:
            input_strategy = FASTQsJoin(
                [build_fastq_strategy(p) for p in input_strategy]
            )
    else:
        raise ValueError(f"Could not parse input_strategy: {repr(input_strategy)}")
    return input_strategy


class _FASTQsBase:

    """
    All FASTQs* strategies
    return a list of tuples of (read1, read2, read3, ...)
    filenames upon being called.

    """

    def __call__(self):
        raise NotImplementedError()  # pragma: no cover

    def _combine_r1_r2(self, forward, reverse):
        results = []
        if not forward:
            raise ValueError(f"No _R1_*.fastq*  files found in {self}")
        if not reverse:
            results.extend(zip(forward))
        if reverse:
            expected_reverse = [Path(str(f).replace("_R1_", "_R2_")) for f in forward]
            if expected_reverse != reverse:
                raise ValueError(
                    f"Error pairing forward/reverse files.\nF:{forward}\nR:{reverse}\nE:{expected_reverse}"
                )
            results.extend(zip(forward, reverse))
        return results

    def _parse_filenames(self, fastqs):
        fastqs = [Path(x).absolute() for x in fastqs]
        forward = sorted([x for x in fastqs if "_R1_" in x.name])
        reverse = sorted([x for x in fastqs if "_R2_" in x.name])
        if not forward and not reverse and fastqs:  # no R1 or R2, but fastqs present
            return sorted(zip(fastqs))
        else:
            return self._combine_r1_r2(forward, reverse)

    @property
    def is_paired(self):
        fastqs = self()
        print("basing pairing on", fastqs)
        print("was paired", len(fastqs[0]) > 1)
        return len(fastqs[0]) > 1


class FASTQsJoin(_FASTQsBase):
    """join files from multiple strategies"""

    def __init__(self, strategies):
        self.strategies = strategies

    def __call__(self):
        res = []
        for s in self.strategies:
            res.extend(s())
        return res


class FASTQsFromFile(_FASTQsBase):
    """Use as single file (or two for paired end) as input"""

    def __init__(self, r1_filename, r2_filename=None):
        self.r1_filename = Path(r1_filename)
        self.r2_filename = Path(r2_filename) if r2_filename else None
        if not self.r1_filename.exists():
            raise IOError(f"file {self.r1_filename} not found")
        if self.r2_filename and not self.r2_filename.exists():
            raise IOError(f"file {self.r2_filename} not found")

    def __call__(self):
        if self.r2_filename:
            return [(self.r1_filename.resolve(), self.r2_filename.resolve())]
        else:
            return [(self.r1_filename.resolve(),)]


class FASTQsFromFiles(_FASTQsBase):
    """Use a list of files"""

    def __init__(self, filenames_r1_and_r2):
        self.filenames = [Path(x) for x in filenames_r1_and_r2]
        for f in self.filenames:
            if not f.exists():
                raise IOError(f"file {f} not found")

    def __call__(self):
        return self._parse_filenames([f.resolve() for f in self.filenames])


class FASTQsFromFolder(_FASTQsBase):
    """Discover fastqs(.gz) in a single folder,
    with automatic pairing based on R1/R2
    """

    def __init__(self, folder):
        self.folder = Path(folder)
        if not self.folder.exists():
            raise IOError(f"folder {self.folder} not found")
        if not hasattr(self, "globs"):
            self.globs = "*.fastq.gz", "*.fastq"
        for g in self.globs:
            if any(self.folder.glob(g)):
                break
        else:
            raise ValueError(
                f"No files matching any of {self.globs} in {self.folder} found"
            )

    def __call__(self):
        fastqs = []
        for g in self.globs:
            fastqs.extend([x.resolve() for x in self.folder.glob(g)])
        return self._parse_filenames(fastqs)

    def __str__(self):
        return f"{self.__class__.__name__}({self.folder})"


class FASTQsFromPrefix(_FASTQsBase):
    """Discover fastqs(.gz) in a single folder,
    which match Prefix.* (* is added by the strategy),
    with automatic pairing based on R1/R2
    """

    def __init__(self, prefix):
        self.folder = Path(prefix).parent
        self.prefix = str(Path(prefix).name)
        if not self.folder.exists():
            raise IOError(f"folder {self.folder} not found")
        if not any(self.folder.glob(self.prefix + "*.fastq.gz")) and not any(
            self.folder.glob(self.prefix + "*.fastq")
        ):
            raise ValueError(
                f"No {self.prefix}*.fastq or {self.prefix}*.fastq.gz in {self.folder} found"
            )

    def __call__(self):
        fastqs = [x.resolve() for x in self.folder.glob(self.prefix + "*.fastq*")]
        return self._parse_filenames(fastqs)

    def __str__(self):
        return f"FASTQsFromPrefix({self.prefix})"


class FASTQsFromJob(_FASTQsBase):
    def __init__(self, job):
        self.dependencies = job
        self.job = job

    def __call__(self):
        return self._parse_filenames(self.job.filenames)

    def __str__(self):
        return f"FASTQsFromJob({self.job})"  # pragma: no cover


class FASTQsFromURLs(_FASTQsBase):
    def __init__(self, urls, job_class=ppg.MultiFileGeneratingJob):
        if isinstance(urls, str):
            urls = [urls]
        self.urls = sorted(urls)
        self.target_files = self.name_files()
        self.job_class = job_class
        self.jobs = self.download_files()
        self.dependencies = self.jobs + [
            ppg.ParameterInvariant(
                hashlib.md5(("".join(self.urls)).encode("utf8")).hexdigest(),
                sorted(self.urls),
            )
        ]

    def __call__(self):
        return self._parse_filenames(self.target_files)

    def name_files(self):
        result = []
        target_dir = Path("incoming") / "automatic"
        key = hashlib.md5()
        for u in self.urls:
            key.update(u.encode("utf8"))
        key = key.hexdigest()
        for u in self.urls:
            if u == "":
                raise ValueError("Empty URL")
            if not ".fastq.gz" in u:  # pragma: no cover
                raise ValueError("Currently limited to .fastq.gz urls", u)
            if "_1.fastq" in u or "_R1_" in u or "_R1.fastq" in u:
                suffix = "_R1_"
            elif "_2.fastq" in u or "_R2_" in u or "_R2.fastq" in u:
                suffix = "_R2_"
            else:
                suffix = ""
            suffix += ".fastq.gz"
            target_filename = target_dir / (key + suffix)
            result.append(target_filename)
        return result

    def download_files(self):
        result = []
        for url, target_fn in zip(self.urls, self.target_files):

            def download(url=url, target_fn=target_fn):
                Path(target_fn).parent.mkdir(exist_ok=True, parents=True)
                target_fn.with_name(target_fn.name + ".url").write_text(url)
                with open(str(target_fn) + "_temp", "wb") as op:
                    download_file(url, op)
                shutil.move(str(target_fn) + "_temp", target_fn)

            job = self.job_class(
                [target_fn, target_fn.with_name(target_fn.name + ".url")], download
            )
            result.append(job)
        return result


class _FASTQsFromSRA(_FASTQsBase):
    def __init__(self, accession, job_class):
        if accession.endswith(":P"):
            self.paired = True
        elif accession.endswith(":S"):
            self.paired = False
        else:
            raise ValueError(
                "Append :P or :S to accession for paired/single end download"
            )
        self.job_class = job_class
        self.accession = accession[:-2]
        self.target_dir = Path("incoming") / "automatic" / accession
        self.target_dir.mkdir(exist_ok=True, parents=True)
        self.cache_dir = Path("cache/sra_temp")
        self.cache_dir.mkdir(exist_ok=True, parents=True)
        self.dependencies = self.fastq_dump()
        import mbf_externals.sratoolkit

        self.algo = mbf_externals.sratoolkit.SRAToolkit()

    def __call__(self):
        # todo: figure out single end lanes
        return [
            (
                str(self.target_dir / self.accession) + "_R1.fastq.gz",
                str(self.target_dir / self.accession) + "_R2.fastq.gz",
            )
        ]

    def fastq_dump(self):
        def dump():
            import subprocess

            cmd = [
                self.algo.path / "bin/" "fasterq-dump",
                "-O",
                str(self.target_dir),
                "-t",
                str(self.cache_dir),
                "-e",
                "4",
            ]
            if self.paired:
                cmd.append("-S")
            cmd.append(self.accession)
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = p.communicate()
            (self.target_dir / "stdout").write_bytes(stdout)
            (self.target_dir / "stderr").write_bytes(stderr)
            if p.returncode != 0 or b"invalid accession" in stderr:
                raise ValueError("fasterq-dump", p.returncode)
            (self.target_dir / "sentinel").write_text("done")

        return self.job_class([self.target_dir / "sentinel"], dump)


def FASTQsFromAccession(
    accession, job_class=ppg.MultiFileGeneratingJob
):  # pragma: no cover - for now
    if accession.startswith("GSM"):
        return _FASTQs_from_url_callback(accession, _urls_for_gsm, job_class)
    # elif accession.startswith("GSE"):#  multilpe
    # raise NotImplementedError()
    elif accession.startswith("SRR"):
        return _FASTQsFromSRA(accession, job_class)
    # elif accession.startswith("E-MTAB"): # multiple!
    # raise NotImplementedError()
    elif accession.startswith("PRJNA"):
        return _FASTQs_from_url_callback(accession, _urls_for_err, job_class)
    elif accession.startswith("DRX"):
        raise NotImplementedError()
    elif accession.startswith("ERR"):
        return _FASTQs_from_url_callback(accession, _urls_for_err, job_class)
    elif accession.startswith("E-MTAB") and ":" in accession:
        return _FASTQs_from_url_callback(accession, _urls_for_emtab, job_class)
    else:
        raise ValueError("Could not handle this accession %s" % accession)


def _urls_for_err(accession):
    ena_url = (
        "http://www.ebi.ac.uk/ena/data/warehouse/filereport?accession=%s&result=read_run&fields=run_accession,fastq_ftp,fastq_md5,fastq_bytes"
        % accession
    )
    r = requests.get(ena_url)
    lines = r.text.strip().split("\n")
    urls = set()
    for line in lines[1:]:
        line = line.split("\t")
        try:
            urls.update(line[1].split(";"))
        except IndexError:
            raise ValueError("No fastq available for {accession} from ENA")
    urls = sorted(["http://" + x for x in urls])
    return urls


def _urls_for_emtab(accession):
    mtab, sample = accession.split(":")
    url = f"https://www.ebi.ac.uk/arrayexpress/files/{mtab}/{mtab}.sdrf.txt"
    r = requests.get(url)
    import io
    import pandas as pd

    df = pd.read_csv(io.StringIO(r.text), sep="\t")
    matching = df[df["Source Name"] == sample]
    if len(matching) == 0:
        raise ValueError("Sample not found in e-mtab", sample, df["Source Name"])
    urls = []
    for c in ["Comment[FASTQ_URI]", "Comment[FASTQ_URI].1"]:
        if c in matching:
            urls.append(matching[c].iloc[0])
    return urls


def _FASTQs_from_url_callback(accession, url_callback, job_class):
    cache_folder = Path("cache/url_lookup")
    cache_folder.mkdir(exist_ok=True, parents=True)
    cache_file = cache_folder / (accession + ".urls")
    if not cache_file.exists():  # pragma: no branch
        cache_file.write_text("\n".join(url_callback(accession)))
    urls = list(set(cache_file.read_text().split("\n")))
    return FASTQsFromURLs(urls, job_class)


def _urls_for_gsm(gsm):
    import re

    url = "http://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=%s" % gsm
    req = requests.get(url, timeout=10)
    page = req.text.strip()
    SRX = re.findall(r">\s*(SRX\d+)\s*<", page)
    if not SRX:
        if ">Reanalysis of<" in page:
            reanalysis = page[page.find(">Reanalysis of<") :]
            reanalysis = reanalysis[: reanalysis.find("</a>")]
            old_gsm = re.findall(r">\s*(GSM\d+)\s*$", reanalysis)
            if not old_gsm:
                raise ValueError(
                    "Could not find SRX, and parsing for reanalysis failed"
                )
            return _urls_for_gsm(old_gsm[0])
        else:
            raise ValueError("Could not find SRX number for gsm '%s'" % gsm)
    if len(set(SRX)) > 1:
        raise ValueError("Found multiple SRX: %s" % SRX)
    SRX = SRX[0]
    srx_url = "https://www.ncbi.nlm.nih.gov/sra?term=%s" % SRX
    req = requests.get(srx_url, timeout=10)
    page = req.text
    SRA = re.findall(r"SRR\d+", page)
    result = []
    for srr in SRA:
        listing_url = "http://ftp.sra.ebi.ac.uk/vol1/fastq/%s/%s/%s/" % (
            srr[:6],
            "00" + srr[-1],
            srr,
        )
        # we could use the http server - but in my experience the ftp server
        # transfers files about 100x faster (20 MB/s vs 200k/s...)
        if "ftp_proxy" in os.environ:
            # but if there is an ftp_proxy, our download code can't make use of it.
            # and we fall back to http
            ftp_url = "http" + listing_url[4:]
        else:
            ftp_url = "ftp" + listing_url[4:]
        req = requests.get(listing_url, timeout=10)
        for filename in re.findall(r'href="([^"]+\.fastq.gz)"', req.text):
            if filename:
                result.append(ftp_url + filename)
        if not result:
            print(listing_url)
    print(result)
    if not result:
        raise ValueError("no fastq found", srx_url, SRA)
    return result


class FASTQsFromMRNAs(_FASTQsBase):
    """turn a bunch of mRNAs from the given genome
    into a fully covering fastq at a given read length

    (mRNA not cDNA, we don't use transcript.cdna but transcript.mrna)
    """

    def __init__(self, transcript_stable_ids, genome, read_length):
        self.key = hashlib.md5(
            f"{transcript_stable_ids} {genome.name} {read_length}".encode("utf-8")
        ).hexdigest()
        self.target_files = [str(Path(f"cache/FASTQsFromCDNAs/{self.key}.fastq"))]
        self.jobs = self.build_file(
            self.target_files[0], transcript_stable_ids, genome, read_length
        )
        self.dependencies = (
            self.jobs
        )  # no need for a ParameterInvariant, it's in the key

    @staticmethod
    def build_file(target_file, transcript_stable_ids, genome, read_length):
        def build(output_filename):
            Path(target_file).parent.mkdir(parents=True, exist_ok=True)
            qual = "z" * read_length
            with open(output_filename, "w") as op:
                for tr in transcript_stable_ids:
                    seq = genome.transcripts[tr].mrna
                    for ii in range(0, len(seq) - read_length + 1):
                        read_name = f"{tr}_{ii}"
                        read = seq[ii : ii + read_length]
                        op.write(f"@{read_name}\n{read}\n+\n{qual}\n")

        return ppg.FileGeneratingJob(target_file, build)

    def __call__(self):
        return self._parse_filenames(self.target_files)


class FASTQsFromMRNAs_Deduplicated(_FASTQsBase):
    """turn a bunch of mRNAs from the given genome
    into a fully covering fastq at a given read length
    For each possible read sequence, only the first instance is written out

    (mRNA not cDNA, we don't use transcript.cdna but transcript.mrna)
    """

    def __init__(self, transcript_stable_ids, genome, read_length):
        self.key = hashlib.md5(
            f"{transcript_stable_ids} {genome.name} {read_length}".encode("utf-8")
        ).hexdigest()
        self.target_files = [str(Path(f"cache/FASTQsFromCDNAs/{self.key}.fastq"))]
        self.jobs = self.build_file(
            self.target_files[0], transcript_stable_ids, genome, read_length
        )
        self.dependencies = (
            self.jobs
        )  # no need for a ParameterInvariant, it's in the key

    @staticmethod
    def build_file(target_file, transcript_stable_ids, genome, read_length):
        def build(output_filename):
            Path(target_file).parent.mkdir(parents=True, exist_ok=True)
            qual = "z" * read_length
            seen = set()
            with open(output_filename, "w") as op:
                for tr in transcript_stable_ids:
                    seq = genome.transcripts[tr].mrna
                    for ii in range(0, len(seq) - read_length + 1):
                        read = seq[ii : ii + read_length]
                        if not read in seen:
                            seen.add(read)
                            read_name = f"{tr}_{ii}"
                            op.write(f"@{read_name}\n{read}\n+\n{qual}\n")

        return ppg.FileGeneratingJob(target_file, build)

    def __call__(self):
        return self._parse_filenames(self.target_files)
