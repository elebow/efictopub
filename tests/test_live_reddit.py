import os

from app.reddit_fetcher import RedditFetcher

if os.environ.get("LIVE_REDDIT") == "true":
    class TestLiveReddit:
        def setup_class(self):
            import configparser
            cfg = configparser.ConfigParser()
            cfg.read("../creds.ini")

            app = cfg.get("DEFAULT", "app")
            secret = cfg.get("DEFAULT", "secret")
            user_agent = cfg.get("DEFAULT", "user_agent")

            self.reddit_fetcher = RedditFetcher(app=app,
                                                secret=secret,
                                                user_agent=user_agent)

        def test_all_submissions_in_list_of_ids(self):
            ids = ["886al5", "88bcar", "88ejcl"]
            subms = self.reddit_fetcher.all_submissions_in_list_of_ids(ids)

            # These values could change!
            assert [len(subm.comments) for subm in subms] == [9, 4, 3]
else:
    pass
