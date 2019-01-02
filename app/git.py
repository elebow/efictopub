import dulwich.porcelain

from app import archive
from app import config

"""Commits archived files to local git repo."""

repo_path = config.archive.location
author = "efictopub <efictopub@users.noreply.github.com>"


def commit_story(story, commit_msg='Update story'):
    filename = archive.path_for_story(story)
    ensure_repo_initialized()

    dulwich.porcelain.add(repo_path, filename)
    dulwich.porcelain.commit(repo_path, message=commit_msg, author=author)


def ensure_repo_initialized():
    try:
        dulwich.porcelain.init(repo_path)
    except FileExistsError:
        pass
