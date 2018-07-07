import requests
import time


DELAY = 1


def get(url):
    """Wait DELAY seconds, then perform an HTTP get request and return the response"""
    time.sleep(DELAY)
    return requests.get(url)
