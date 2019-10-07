import argparse

from efictopub import fetchers


class AliasFetcherOpt(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if namespace.fetcher_opts is None:
            namespace.fetcher_opts = []

        namespace.fetcher_opts.append(f"{self.dest}={values}")


parser = argparse.ArgumentParser(
    prog="efictopub",
    description="Fetch stories from various sources and optionally generate an "
    "EPUB file.",
)

parser.add_argument(
    "target",
    type=str,
    help="target story or document containing list of stories (URL, reddit ID, etc). "
    "Automatic fetcher selection is supported only for URLs.",
)

parser.add_argument(
    "--fetcher",
    "-F",
    type=str,
    dest="fetcher",
    action="store",
    help=f"manually specify fetcher to use ({', '.join(fetchers.fetcher_names())})",
)

parser.add_argument(
    "--config",
    "-c",
    dest="config_file",
    action="store",
    help=f"override default config file",
)
parser.add_argument(
    "--outfile",
    "-o",
    dest="outfile",
    action="store",
    help=f"specify output file, for actions that support an output file (default varies per action)",
)

parser.add_argument(
    "--no-archive",
    dest="write_archive",
    action="store_false",
    default=True,
    help="do not write the story to the archive",
)
parser.add_argument(
    "--clobber",
    dest="clobber",
    action="store_true",
    default=False,
    help="clobber uncommitted changes in the archive",
)
parser.add_argument(
    "--no-comments",
    dest="comments",
    action="store_false",
    default=True,
    help="do not store or write comments, for fetchers that support comments",
)
parser.add_argument(
    "--no-write-epub",
    dest="write_epub",
    action="store_false",
    default=True,
    help="do not write an EPUB file",
)

parser.add_argument(
    "--fetcher-opt",
    dest="fetcher_opts",
    action="append",
    help="extra options passed through to fetchers",
)
parser.add_argument(
    "--title", "-t", action=AliasFetcherOpt, help="manually specify story title"
)
parser.add_argument(
    "--author", "-a", action=AliasFetcherOpt, help="manually specify story author"
)


def get():
    return vars(parser.parse_args())
