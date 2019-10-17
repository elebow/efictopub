import dulwich.porcelain

from efictopub import config
from efictopub import git


class TestGit:
    def test_commit_story(self, mocker, story_factory):
        mocker.patch("efictopub.git.ensure_repo_initialized")
        mocker.patch("dulwich.porcelain.commit")
        mocker.patch("dulwich.porcelain.add")
        config.config["archive_location"] = "/path/to/archive"
        story = story_factory.build()

        git.commit_story(story)

        git.ensure_repo_initialized.assert_called_once()
        dulwich.porcelain.add.assert_called_once_with(
            "/path/to/archive", f"/path/to/archive/{story.id}.json"
        )
        dulwich.porcelain.commit.assert_called_once_with(
            "/path/to/archive",
            message="Update story",
            author="efictopub <efictopub@users.noreply.github.com>",
        )

    def test_repo_is_dirty_dirty(self, mocker):
        mocker.patch("efictopub.git.ensure_repo_initialized")
        mocker.patch(
            "dulwich.porcelain.status",
            lambda _x: dulwich.porcelain.GitStatus(
                staged={"add": [], "delete": [], "modify": []},
                unstaged=[b"f1"],
                untracked=[],
            ),
        )
        config.config["archive_location"] = "/path/to/archive"

        assert git.repo_is_dirty() is True

    def test_repo_is_dirty_clean(self, mocker):
        mocker.patch("efictopub.git.ensure_repo_initialized")
        mocker.patch(
            "dulwich.porcelain.status",
            lambda _x: dulwich.porcelain.GitStatus(
                staged={"add": [], "delete": [], "modify": []},
                unstaged=[],
                untracked=[],
            ),
        )
        mocker.patch("efictopub.git.repo_path", lambda: "/path/to/archive")
        config.config["archive_location"] = "/path/to/archive"

        assert git.repo_is_dirty() is False

    def test_previous_commit_is_not_efic_true(self, mocker, story_factory):
        mocker.patch(
            "dulwich.repo.Repo.get_walker",
            lambda _x, **args: [
                mocker.MagicMock(
                    commit=mocker.MagicMock(author=b"some other committer")
                )
            ],
        )
        story = story_factory.build()

        assert git.previous_commit_is_not_efic(story) is True

    def test_previous_commit_is_not_efic_false(self, mocker, story_factory):
        mocker.patch(
            "dulwich.repo.Repo.get_walker",
            lambda _x, **args: [
                mocker.MagicMock(
                    commit=mocker.MagicMock(
                        author=b"efictopub <efictopub@users.noreply.github.com>"
                    )
                )
            ],
        )
        story = story_factory.build()

        assert git.previous_commit_is_not_efic(story) is False
