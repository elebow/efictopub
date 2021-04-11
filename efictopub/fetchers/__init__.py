from collections import namedtuple
import pkgutil
import importlib

from .base_fetcher import BaseFetcher
from efictopub.exceptions import NoFetcherForUrlError, UnknownFetcherError

fetchers = []
Fetcher = namedtuple("Fetcher", ["fetcher_module", "can_handle_url"])

for module_info in pkgutil.iter_modules(__path__, prefix="efictopub.fetchers."):
    module = importlib.import_module(module_info.name)
    if hasattr(module, "Fetcher"):
        fetchers.append(Fetcher(module, module.can_handle_url))


def fetcher_by_name(name, url):
    full_name = f"efictopub.fetchers.{name}"
    for fetcher in fetchers:
        if fetcher.fetcher_module.__name__ == full_name:
            return fetcher.fetcher_module.Fetcher(url)

    raise UnknownFetcherError(f"Unknown fetcher `{name}`")


def fetcher_for_url(url):
    for fetcher in fetchers:
        if fetcher.can_handle_url(url):
            return fetcher.fetcher_module.Fetcher(url)

    raise NoFetcherForUrlError(f"Couldn't find a fetcher that can handle `{url}`")


def fetcher_names():
    return [fetcher.fetcher_module.__name__ for fetcher in fetchers]
