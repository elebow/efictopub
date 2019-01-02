from unittest.mock import MagicMock
from unittest.mock import patch

from app import git


from tests.fixtures.doubles import story_double


class TestGit:
    @patch("app.config.archive", MagicMock(location="/path/to/archive"))
    @patch("app.git.repo_path", "/path/to/archive")
    @patch("app.git.ensure_repo_initialized")
    @patch("dulwich.porcelain.commit")
    @patch("dulwich.porcelain.add")
    def test_commit_story(self, add, commit, ensure_repo_initialized):
        story = story_double()

        git.commit_story(story)

        ensure_repo_initialized.assert_called_once()
        add.assert_called_once_with("/path/to/archive", f"/path/to/archive/{story.id}.yml")
        commit.assert_called_once_with("/path/to/archive",
                                       message="Update story",
                                       author="efictopub <efictopub@users.noreply.github.com>")
