from efictopub.cli import opts


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

    def test_config_file(self, mocker):
        mocker.patch("sys.argv", ["executable_name", "www.example.com/target"])
        options = opts.get()

        assert options["write_archive"] is True
        assert "archive_location" not in options

    def test_cli_arg_overrides_config_file(self, mocker):
        mocker.patch(
            "sys.argv", ["executable_name", "www.example.com/target", "--no-archive"]
        )
        options = opts.get()

        assert options["write_archive"] is False
