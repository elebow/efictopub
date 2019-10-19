from efictopub.models.ffnet.ffnet_reviews import FFNetReviews

import pytest

from tests.fixtures.real import ffnet_chapter_reviews_html_real


class TestFFNetReviews:
    @pytest.fixture
    def reviews(self):
        return FFNetReviews(ffnet_chapter_reviews_html_real).reviews

    def test_as_comment(self, reviews):
        assert [r.author for r in reviews] == [
            "User 201",
            "User 202",
            "User 203",
            "User 204",
            "User 205",
            "User 206",
        ]

        assert [r.date_published.timestamp() for r in reviews] == [
            1525044182,
            1502099520,
            1496473762,
            1494499329,
            1494441199,
            1492430074,
        ]

        assert [r.text for r in reviews] == [
            "Review 1 content",
            "Review 2 content",
            "Review 3 content with\nline break",
            "Review 4 content",
            "Review 5 content",
            "Review 6 content",
        ]
