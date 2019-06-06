import os

from app import fetchers

if os.environ.get("LIVE_REDDIT") == "true":

    class TestLiveReddit:
        def setup_class(self):
            import configparser

            cfg = configparser.ConfigParser()
            cfg.read("../creds.ini")

            self.reddit_fetcher = fetchers.Reddit()

        def test_submissions_in_list_of_ids(self):
            ids = ["886al5", "88bcar", "88ejcl"]
            subms = self.reddit_fetcher.submissions_in_list_of_ids(ids)

            # These values could change!
            assert [len(subm.comments) for subm in subms] == [9, 4, 3]


else:
    pass
