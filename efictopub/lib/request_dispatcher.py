from pathlib import Path
import random
import requests
import time
import urllib

from efictopub import config


MIN_DELAY = 155


def get(url):
    if not config.get("force_fetch") and is_url_in_cache(url):
        return read_cache(url)

    contents = get_from_remote(url).text
    write_cache(url, contents)
    return contents


def get_from_remote(url):
    """Wait MIN_DELAY to 2*MIN_DELAY seconds, then perform an HTTP get request and return the response"""
    delay = MIN_DELAY + random.random() * MIN_DELAY
    time.sleep(delay)

    return requests.get(url, headers={"User-Agent": config.get("user_agent")})


def is_url_in_cache(url):
    return cache_path_for_url(url).exists()


def read_cache(url):
    return cache_path_for_url(url).read_text()


def write_cache(url, contents):
    ensure_cache_dir_exists()
    return cache_path_for_url(url).write_text(contents)


def cache_path_for_url(url):
    return Path(f"{config.get('http_cache_location')}/{urllib.parse.quote_plus(url)}")


def ensure_cache_dir_exists():
    cache_path = Path(config.get("http_cache_location"))
    if not cache_path.exists():
        cache_path.mkdir(parents=True)
