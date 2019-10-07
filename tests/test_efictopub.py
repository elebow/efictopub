from doubles import allow
from unittest.mock import call
from unittest.mock import MagicMock
from unittest.mock import patch

from efictopub import config
from efictopub import git
from efictopub.models.reddit import RedditSubmission
from efictopub.efictopub import Efictopub

from tests.fixtures.doubles import praw_submissions_double, story_double


class TestEfictopub:
    def setup_method(self):
        config.config["fetcher_opts"] = ["title='Great Story'"]
