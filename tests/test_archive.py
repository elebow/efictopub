import pytest

from efictopub import archive
from efictopub import config
from efictopub.exceptions import NoArchivedStoryError, AmbiguousArchiveIdError


class TestArchive:
    ID = "55555-my-great-story-id"

    def test_get(self, mocker):
        mocker.patch("efictopub.archive.id_or_path_to_path", lambda x: "my-great-path")
        jsonpickle_decode = mocker.patch("jsonpickle.decode")
        mocker.patch("builtins.open", new_callable=mocker.mock_open)

        archive.get(self.ID)

        open.assert_called_once_with("my-great-path", "r")
        jsonpickle_decode.assert_called_once_with(open().read())

    def test_store(self, mocker):
        git_commit_story = mocker.patch("efictopub.git.commit_story")
        jsonpickle_encode = mocker.patch("jsonpickle.encode")
        mocker.patch("builtins.open", new_callable=mocker.mock_open)

        story = mocker.MagicMock(id="my-great-path", title="great-story", text="hhh")
        config.config["archive_location"] = "/path/to/archive"
        archive.store(story)

        open.assert_called_once_with("/path/to/archive/my-great-path.json", "w")
        jsonpickle_encode.assert_called_once_with(story)
        git_commit_story.assert_has_calls(
            [
                mocker.call(story, "Local changes before fetching great-story"),
                mocker.call(story, "Fetch great-story"),
            ]
        )

    def test_path_zero_matches_found(self, mocker):
        mocker.patch("glob.glob", lambda x: [])

        with pytest.raises(NoArchivedStoryError):
            archive.id_or_path_to_path(self.ID)

    def test_path_one_match_found(self, mocker):
        mocker.patch(
            "glob.glob", lambda x: ["/whatever/path/to/55555-my-great-story-id.json"]
        )

        assert (
            archive.id_or_path_to_path(self.ID)
            == "/whatever/path/to/55555-my-great-story-id.json"
        )

    def test_path_many_matches_found(self, mocker):
        mocker.patch("glob.glob", lambda x: ["/whatever/1", "/whatever/2"])

        with pytest.raises(AmbiguousArchiveIdError):
            archive.id_or_path_to_path(self.ID)

    def test_path_partial_id(self, mocker):
        mocker.patch("glob.glob", lambda x: ["55555-my-great-story-id.json"])

        assert archive.id_or_path_to_path("55") == "55555-my-great-story-id.json"
