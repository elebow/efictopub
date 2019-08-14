import random
import requests
import time


MIN_DELAY = 1


def get(url):
    """Wait MIN_DELAY to 2*MIN_DELAY seconds, then perform an HTTP get request and return the response"""
    delay = MIN_DELAY + random.random() * MIN_DELAY
    time.sleep(delay)
    return requests.get(url)
