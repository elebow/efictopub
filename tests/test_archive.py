import os
from unittest.mock import mock_open
from unittest.mock import patch


from app.archive import Archive


class TestArchive:

    def setup_class(self):
        self.id = "55555-my-great-story-id"

    def setup_method(self):
        self.subject = Archive()

    @patch("app.archive.Archive.path", lambda x: "my-great-path")
    @patch("yaml.safe_load")
    @patch("builtins.open", new_callable=mock_open)
    def test_get(self, file_open, yaml_safe_load):
        self.subject.get(self.id)

        file_open.assert_called_once_with("my-great-path", "r")
        yaml_safe_load.assert_called_once_with(file_open())

    @patch("app.archive.Archive.path", lambda x: "my-great-path")
    @patch("yaml.dump")
    @patch("builtins.open", new_callable=mock_open)
    def test_store(self, file_open, yaml_dump):
        self.subject.store(self.id, "hhh")

        file_open.assert_called_once_with("my-great-path", "w")
        yaml_dump.assert_called_once_with("hhh", file_open())

    def test_path(self):
        assert self.subject.path(self.id) == f"{os.environ.get('HOME')}/.reddit_series/cache/55555-my-great-story-id.yml"
