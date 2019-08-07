import dulwich
import dulwich.porcelain

from app import archive
from app.config import config

"""Commits archived files to local git repo."""

repo_path = config["archive_location"].get()
efic_author = "efictopub <efictopub@users.noreply.github.com>"


def commit_story(story, commit_msg="Update story"):
    filename = archive.path_for_story(story)
    ensure_repo_initialized()

    dulwich.porcelain.add(repo_path, filename)
    dulwich.porcelain.commit(repo_path, message=commit_msg, author=efic_author)


def repo_is_dirty():
    """Return true if the git repo has any uncommitted changes, which we don't want to clobber."""
    status = dulwich.porcelain.status(repo_path)
    return (
        len(status.staged["add"]) > 0
        or len(status.staged["delete"]) > 0
        or len(status.staged["modify"]) > 0
        or len(status.unstaged) > 0
        or len(status.untracked) > 0
    )


def previous_commit_is_not_efic(story):
    filename = archive.path_for_story(story).encode()
    authors = [
        entry.commit.author.decode()
        for entry in dulwich.repo.Repo(".").get_walker(paths=[filename], max_entries=2)
    ]

    return any([author != efic_author for author in authors])


def ensure_repo_initialized():
    try:
        dulwich.porcelain.init(repo_path)
    except FileExistsError:
        pass
