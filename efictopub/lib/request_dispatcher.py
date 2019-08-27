import random
import requests
import time

from efictopub import config


MIN_DELAY = 1


def get(url):
    """Wait MIN_DELAY to 2*MIN_DELAY seconds, then perform an HTTP get request and return the response"""
    delay = MIN_DELAY + random.random() * MIN_DELAY
    time.sleep(delay)

    return requests.get(url, headers=get_headers())


def get_headers():
    return {"User-Agent": config.get("user_agent")}
