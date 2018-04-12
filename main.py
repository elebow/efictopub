#!/usr/bin/python3

import json

from submission_collector import SubmissionCollector


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
                                         user_agent=user_agent)
    print(json.dumps(subm_collector.all_submissions_by_author_name(sys.argv[2])))
