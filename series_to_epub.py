#!/usr/bin/python3

import json
import praw


class SubmissionCollector:
    def __init__(self, *, app, secret, user_agent, target_name):
        self.reddit = praw.Reddit(client_id=app, client_secret=secret, user_agent=user_agent)
        self.target = self.reddit.redditor(target_name)

    def all_submissions_as_json(self):
        return json.dumps(
            [{"post": self.filter_subm(subm), "comments": self.all_comments_for_subm(subm)}
                for subm
                in self.target.submissions.new(limit=3)]
        )

    def all_comments_for_subm(self, subm):
        subm.comments.replace_more(limit=None)
        return [self.comment_tree(comm) for comm in subm.comments]

    def comment_tree(self, comm):
        if len(comm.replies) == 0:
            return self.filter_comm(comm)
        else:
            return {
                "comment": self.filter_comm(comm),
                "replies": [self.comment_tree(c) for c in comm.replies]
            }

    def filter_comm(self, comm):
        comm.__dict__["author"] = comm.author.name  # replace author obj with a string
        #if comm.__dict__["edited"] is False:
        #    del comm.__dict__["edited"]
        wanted_keys = ["author", "created_utc", "body", "edited", "permalink"]
        return {k: v for k, v in comm.__dict__.items() if k in wanted_keys}

    def filter_subm(self, subm):
        subm.__dict__["author"] = subm.author.name  # replace author obj with a string
        wanted_keys = ["author", "title", "created_utc", "selftext", "edited", "permalink"]
        return {k: v for k, v in subm.__dict__.items() if k in wanted_keys}


if __name__ == "__main__":
    import configparser
    import sys

    cfg = configparser.ConfigParser()
    cfg.read(sys.argv[1])
    app = cfg.get('DEFAULT', 'app')
    secret = cfg.get('DEFAULT', 'secret')
    user_agent = cfg.get("DEFAULT", "user_agent")

    subm_collector = SubmissionCollector(app=app,
                                         secret=secret,
                                         user_agent=user_agent,
                                         target_name=sys.argv[2])
    print(subm_collector.all_submissions_as_json())
