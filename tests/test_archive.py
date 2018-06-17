import pytest
from unittest.mock import MagicMock
from unittest.mock import mock_open
from unittest.mock import patch


from app import archive
from app.exceptions import NoArchivedStoryError, AmbiguousArchiveIdError


class TestArchive:

    def setup_class(self):
        self.id = "55555-my-great-story-id"

    @patch("app.archive.id_or_path_to_path", lambda x: "my-great-path")
    @patch("yaml.safe_load")
    @patch("builtins.open", new_callable=mock_open)
    def test_get(self, file_open, yaml_safe_load):
        archive.get(self.id)

        file_open.assert_called_once_with("my-great-path", "r")
        yaml_safe_load.assert_called_once_with(file_open())

    @patch("app.config.archive", MagicMock(location="/path/to/archive"))
    @patch("yaml.safe_dump")
    @patch("builtins.open", new_callable=mock_open)
    def test_store(self, file_open, yaml_dump):
        story = MagicMock(id="my-great-path", text="hhh")
        archive.store(story)

        file_open.assert_called_once_with("/path/to/archive/my-great-path.yml", "w")
        yaml_dump.assert_called_once_with(story, file_open())

    @patch("glob.glob", lambda x: [])
    def test_path_zero_matches_found(self):
        with pytest.raises(NoArchivedStoryError):
            archive.id_or_path_to_path(self.id)

    @patch("glob.glob", lambda x: ["/whatever/path/to/55555-my-great-story-id.yml"])
    def test_path_one_match_found(self):
        assert archive.id_or_path_to_path(self.id) == "/whatever/path/to/55555-my-great-story-id.yml"

    @patch("glob.glob", lambda x: ["/whatever/1", "/whatever/2"])
    def test_path_many_matches_found(self):
        with pytest.raises(AmbiguousArchiveIdError):
            archive.id_or_path_to_path(self.id)

    @patch("glob.glob", lambda x: ["55555-my-great-story-id.yml"])
    def test_path_partial_id(self):
        assert archive.id_or_path_to_path("55") == "55555-my-great-story-id.yml"
