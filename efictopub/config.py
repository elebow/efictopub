# Module to store and retrieve app-wide config values

import functools
import os

from efictopub.exceptions import MissingRequiredFetcherOptError

# Config value precedence, from lowest to highest:
#   - The nested structure in the config file, except for `overrides`.
#   - Any values specified under `overrides` for the chosen fetcher
#   - Any values specified on the command line

# See https://confuse.readthedocs.io/en/latest/#search-paths for config file locations


def load(opts, *, fetcher):
    global config
    config = opts


def get(key):
    global config
    if isinstance(key, str):
        value = config.get(key)
    elif isinstance(key, list):
        # chain of nested config items
        value = functools.reduce(dict.__getitem__, key, config)

    return expand_vars(value)


def get_fetcher_opt(key, required=False):
    fetcher_opts = config.get("fetcher_opts")
    if fetcher_opts:
        matching_opts = [opt for opt in fetcher_opts if opt.startswith(f"{key}=")]

        if matching_opts:
            # the last one "wins"
            return matching_opts[-1].split("=")[-1]

    if required:
        raise MissingRequiredFetcherOptError(key)


def expand_vars(value):
    # Expand any env vars in the string, respecting XDG

    if not isinstance(value, str):
        return value

    # XDG requires us to substitute values for certain variable names, even if they are not defined
    # see https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html
    old_environ = os.environ.copy()
    try:
        os.environ["XDG_DATA_HOME"] = f"{old_environ['HOME']}/.local/share"
        os.environ["XDG_CONFIG_HOME"] = f"{old_environ['HOME']}/.config"
        os.environ["XDG_DATA_DIRS"] = "/usr/local/share/:/usr/share/"
        os.environ["XDG_CONFIG_DIRS"] = "/etc/xdg"
        os.environ["XDG_CACHE_HOME"] = f"{old_environ['HOME']}/.cache"

        value = os.path.expandvars(value)
    finally:
        os.environ.clear()
        os.environ.update(old_environ)

    return value
