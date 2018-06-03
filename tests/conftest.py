import os
import pytest
from unittest.mock import MagicMock

import app.lib.reddit_util

if os.environ.get("LIVE_REDDIT") != "true":
    @pytest.fixture(autouse=True, scope="session")
    def no_hit_reddit():
        app.lib.reddit_util.setup_reddit = MagicMock()
