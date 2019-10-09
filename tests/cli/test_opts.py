import confuse

from unittest.mock import patch

from efictopub.cli import opts


def load_config_file():
    conf = confuse.Configuration("efictopub", read=False)
    conf.set_file("tests/fixtures/config.yaml")
    return conf


class TestCliOpts:
    def test_parser(self):
        args = opts.parser.parse_args(
            [
                "www.example.com/great-story",
                "--no-write-epub",
                *["--title", "My Great Title"],
            ]
        )

        assert args.target == "www.example.com/great-story"
        assert args.write_epub is False
        assert "title=My Great Title" in args.fetcher_opts

    @patch("efictopub.cli.opts.load_config_file", load_config_file)
    @patch("sys.argv", ["executable_name", "www.example.com/target"])
    def test_config_file(self):
        options = opts.get()

        assert options["write_archive"] is True
        assert options["archive_location"] == "/path/to/archive"

    @patch("efictopub.cli.opts.load_config_file", load_config_file)
    @patch("sys.argv", ["executable_name", "www.example.com/target", "--no-archive"])
    def test_cli_arg_overrides_config_file(self):
        options = opts.get()

        assert options["write_archive"] is False
