#!/usr/bin/python3

# Test the fetching and parsing functionality by running efictopub against real live
# sites. The expected values are stored in a file outside the repo for copyright
# reasons.

import yaml

from efictopub.efictopub import Efictopub


def verify_equal(actual, expected):
    if not actual == expected:
        raise Exception(
            f"actual value `{actual}` is not equal to expected value `{expected}`"
        )


with open("real_live_tests.yaml", "r") as test_cases_file:
    test_cases = yaml.load(test_cases_file)

for test_name, test_case in test_cases.items():
    print(f"testing {test_name}")

    args = {"target": test_case["target"]}

    if "title" in test_case:
        args["title"] = test_case["title"]

    story = Efictopub(args).story

    verify_equal(story.title, test_case["expected"]["title"])
    verify_equal(story.author, test_case["expected"]["author"])
    verify_equal(story.summary, test_case["expected"]["summary"])
    verify_equal(
        sum([len(chapter.text) for chapter in story.chapters]),
        test_case["expected"]["text_size"],
    )
    verify_equal(story.chapters[-1].text[-50:], test_case["expected"]["last_50_chars"])

print("[32mtests complete[0m")
