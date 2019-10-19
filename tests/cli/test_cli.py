from efictopub.cli import cli

import pytest


class TestCliCli:
    @pytest.fixture(autouse=True)
    def efictopub_obj(self, mocker):
        return mocker.patch("efictopub.cli.cli.Efictopub.__new__")

    def test_run(self, mocker, efictopub_obj):
        mocker.patch(
            "efictopub.cli.opts.get",
            lambda: {"write_archive": True, "write_epub": True},
        )
        cli.run()

        efictopub_obj.assert_called_once()
        efictopub_obj().archive_story.assert_called_once()
        efictopub_obj().write_epub.assert_called_once()

    def test_run_no_archive(self, mocker, efictopub_obj):
        mocker.patch(
            "efictopub.cli.opts.get",
            lambda: {"write_archive": False, "write_epub": True},
        )

        cli.run()

        efictopub_obj.assert_called_once()
        efictopub_obj().archive_story.assert_not_called()
        efictopub_obj().write_epub.assert_called_once()

    def test_run_no_archive_archive_fetcher(self, mocker, efictopub_obj):
        mocker.patch(
            "efictopub.cli.opts.get",
            lambda: {"write_archive": True, "write_epub": True},
        )
        efictopub_obj().fetcher.__module__ = "archive"
        efictopub_obj().reset_mock()  # reset because we just called it when setting the fetcher module
        cli.run()

        efictopub_obj.assert_called()
        efictopub_obj().archive_story.assert_not_called()
        efictopub_obj().write_epub.assert_called_once()

    def test_run_no_epub(self, mocker, efictopub_obj):
        mocker.patch(
            "efictopub.cli.opts.get",
            lambda: {"write_archive": True, "write_epub": False},
        )

        cli.run()

        efictopub_obj.assert_called_once()
        efictopub_obj().archive_story.assert_called_once()
        efictopub_obj().write_epub.assert_not_called()

    def test_run_no_archive_or_epub(self, mocker, efictopub_obj):
        mocker.patch(
            "efictopub.cli.opts.get",
            lambda: {"write_archive": False, "write_epub": False},
        )

        cli.run()

        efictopub_obj.assert_called_once()
        efictopub_obj().archive_story.assert_not_called()
        efictopub_obj().write_epub.assert_not_called()
