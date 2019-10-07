from dulwich.porcelain import GitStatus

from unittest.mock import MagicMock
from unittest.mock import patch

from efictopub import config
from efictopub import git

from tests.fixtures.doubles import story_double


class TestGit:
    @patch("efictopub.git.repo_path", lambda: "/path/to/archive")
    @patch("efictopub.git.ensure_repo_initialized")
    @patch("dulwich.porcelain.commit")
    @patch("dulwich.porcelain.add")
    def test_commit_story(self, add, commit, ensure_repo_initialized):
        config.config["archive_location"] = "/path/to/archive"
        story = story_double()

        git.commit_story(story)

        ensure_repo_initialized.assert_called_once()
        add.assert_called_once_with(
            "/path/to/archive", f"/path/to/archive/{story.id}.json"
        )
        commit.assert_called_once_with(
            "/path/to/archive",
            message="Update story",
            author="efictopub <efictopub@users.noreply.github.com>",
        )

    @patch("efictopub.git.repo_path", lambda: "/path/to/archive")
    @patch("efictopub.git.ensure_repo_initialized", MagicMock())
    @patch(
        "dulwich.porcelain.status",
        lambda _x: GitStatus(
            staged={"add": [], "delete": [], "modify": []},
            unstaged=[b"f1"],
            untracked=[],
        ),
    )
    def test_repo_is_dirty_dirty(self):
        assert git.repo_is_dirty() is True

    @patch("efictopub.git.repo_path", lambda: "/path/to/archive")
    @patch("efictopub.git.ensure_repo_initialized", MagicMock())
    @patch(
        "dulwich.porcelain.status",
        lambda _x: GitStatus(
            staged={"add": [], "delete": [], "modify": []}, unstaged=[], untracked=[]
        ),
    )
    def test_repo_is_dirty_clean(self):
        assert git.repo_is_dirty() is False

    @patch(
        "dulwich.repo.Repo.get_walker",
        lambda _x, **args: [
            MagicMock(commit=MagicMock(author=b"some other committer"))
        ],
    )
    def test_previous_commit_is_not_efic_true(self):
        story = story_double()
        assert git.previous_commit_is_not_efic(story) is True

    @patch(
        "dulwich.repo.Repo.get_walker",
        lambda _x, **args: [
            MagicMock(
                commit=MagicMock(
                    author=b"efictopub <efictopub@users.noreply.github.com>"
                )
            )
        ],
    )
    def test_previous_commit_is_not_efic_false(self):
        story = story_double()
        assert git.previous_commit_is_not_efic(story) is False
