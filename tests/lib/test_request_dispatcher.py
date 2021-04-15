import pytest

from efictopub import config
from efictopub.lib import request_dispatcher


class TestRequestDispatcher:
    @pytest.fixture(autouse=True)
    def disable_force_fetch(self):
        config.config["force_fetch"] = False

    def test_get(self, requests_mock):
        config.config["force_fetch"] = False
        requests_mock.get(
            "https://example.com/1",
            text="example 1",
        )

        request_dispatcher.get("https://example.com/1")
        request_dispatcher.get("https://example.com/1")

        assert requests_mock.call_count == 1

        with open(request_dispatcher.cache_path_for_url("https://example.com/1")) as f:
            assert f.read() == "example 1"
