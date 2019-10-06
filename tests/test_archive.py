import pytest
from unittest.mock import call
from unittest.mock import MagicMock
from unittest.mock import mock_open
from unittest.mock import patch


from efictopub import archive
from efictopub import config
from efictopub.exceptions import NoArchivedStoryError, AmbiguousArchiveIdError


class TestArchive:
    def setup_class(self):
        self.id = "55555-my-great-story-id"

    @patch("efictopub.archive.id_or_path_to_path", lambda x: "my-great-path")
    @patch("jsonpickle.decode")
    @patch("builtins.open", new_callable=mock_open)
    def test_get(self, file_open, jsonpickle_decode):
        archive.get(self.id)

        file_open.assert_called_once_with("my-great-path", "r")
        jsonpickle_decode.assert_called_once_with(file_open().read())

    @patch("efictopub.git.commit_story")
    @patch("jsonpickle.encode")
    @patch("builtins.open", new_callable=mock_open)
    def test_store(self, file_open, jsonpickle_encode, git_commit_story):
        story = MagicMock(id="my-great-path", title="great-story", text="hhh")
        config.config["archive_location"] = "/path/to/archive"
        archive.store(story)

        file_open.assert_called_once_with("/path/to/archive/my-great-path.json", "w")
        jsonpickle_encode.assert_called_once_with(story)
        git_commit_story.assert_has_calls(
            [
                call(story, "Local changes before fetching great-story"),
                call(story, "Fetch great-story"),
            ]
        )

    @patch("glob.glob", lambda x: [])
    def test_path_zero_matches_found(self):
        with pytest.raises(NoArchivedStoryError):
            archive.id_or_path_to_path(self.id)

    @patch("glob.glob", lambda x: ["/whatever/path/to/55555-my-great-story-id.json"])
    def test_path_one_match_found(self):
        assert (
            archive.id_or_path_to_path(self.id)
            == "/whatever/path/to/55555-my-great-story-id.json"
        )

    @patch("glob.glob", lambda x: ["/whatever/1", "/whatever/2"])
    def test_path_many_matches_found(self):
        with pytest.raises(AmbiguousArchiveIdError):
            archive.id_or_path_to_path(self.id)

    @patch("glob.glob", lambda x: ["55555-my-great-story-id.json"])
    def test_path_partial_id(self):
        assert archive.id_or_path_to_path("55") == "55555-my-great-story-id.json"
