from unittest.mock import patch

from efictopub.cli import cli


@patch("efictopub.cli.cli.Efictopub.__new__")
class TestCliCli:
    @patch(
        "efictopub.cli.opts.get", lambda: {"write_archive": True, "write_epub": True}
    )
    def test_run(self, efictopub_obj):
        cli.run()

        efictopub_obj.assert_called_once()
        efictopub_obj().archive_story.assert_called_once()
        efictopub_obj().write_epub.assert_called_once()

    @patch(
        "efictopub.cli.opts.get", lambda: {"write_archive": False, "write_epub": True}
    )
    def test_run_no_archive(self, efictopub_obj):
        cli.run()

        efictopub_obj.assert_called_once()
        efictopub_obj().archive_story.assert_not_called()
        efictopub_obj().write_epub.assert_called_once()

    @patch(
        "efictopub.cli.opts.get", lambda: {"write_archive": True, "write_epub": True}
    )
    def test_run_no_archive_archive_fetcher(self, efictopub_obj):
        efictopub_obj().fetcher.__module__ = "archive"
        efictopub_obj().reset_mock()  # reset because we just called it when setting the fetcher module
        cli.run()

        efictopub_obj.assert_called()
        efictopub_obj().archive_story.assert_not_called()
        efictopub_obj().write_epub.assert_called_once()

    @patch(
        "efictopub.cli.opts.get", lambda: {"write_archive": True, "write_epub": False}
    )
    def test_run_no_epub(self, efictopub_obj):
        cli.run()

        efictopub_obj.assert_called_once()
        efictopub_obj().archive_story.assert_called_once()
        efictopub_obj().write_epub.assert_not_called()

    @patch(
        "efictopub.cli.opts.get", lambda: {"write_archive": False, "write_epub": False}
    )
    def test_run_no_archive_or_epub(self, efictopub_obj):
        cli.run()

        efictopub_obj.assert_called_once()
        efictopub_obj().archive_story.assert_not_called()
        efictopub_obj().write_epub.assert_not_called()
