#!/bin/sh
pipenv run python3 -m pytest -s --cov=app
# -s         do not capture output. This is needed for ipdb.set_trace()
# --cov=app  show code coverage for the dir `app`
