from collections import namedtuple
import pkgutil

from .base_fetcher import BaseFetcher
from app.exceptions import NoFetcherForUrlError, UnknownFetcherError

fetchers = []
Fetcher = namedtuple("Fetcher", ["fetcher_module", "fetcher_class", "can_handle_url"])

for module_info in pkgutil.iter_modules(__path__):
    module = module_info.module_finder.find_loader(module_info.name)[0].load_module()
    if hasattr(module, "FETCHER_CLASS"):
        fetcher_class = getattr(module, "FETCHER_CLASS")

        # Add it to locals() so we can reference it from elsewhere.
        # This is equivalent to doing a bunch of `from .archive import Archive`
        # TODO is this even necessary
        locals()[fetcher_class.__name__] = fetcher_class

        fetchers.append(Fetcher(module, fetcher_class, module.can_handle_url))


def fetcher_by_name(name, url):
    for fetcher in fetchers:
        if fetcher.fetcher_module.__name__ == name:
            return fetcher.fetcher_class(url)

    raise UnknownFetcherError(f"Unknown fetcher `{name}`")


def fetcher_for_url(url):
    for fetcher in fetchers:
        if fetcher.can_handle_url(url):
            return fetcher.fetcher_class(url)

    raise NoFetcherForUrlError(f"Couldn't find a fetcher that can handle `{url}`")


def fetcher_names():
    return [fetcher.fetcher_module.__name__ for fetcher in fetchers]
