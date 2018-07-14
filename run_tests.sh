#!/bin/sh
pipenv run python3 -m pytest \
    --cov=app   # show code coverage for the dir `app`
