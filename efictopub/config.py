# Module to store and retrieve app-wide config values

import functools

from efictopub.exceptions import MissingRequiredFetcherOptError

# Config value precedence, from lowest to highest:
#   - The nested structure in the config file, except for `overrides`.
#   - Any values specified under `overrides` for the chosen fetcher
#   - Any values specified on the command line

# See https://confuse.readthedocs.io/en/latest/#search-paths for config file locations


def load(opts, *, fetcher):
    global config
    config = opts
    apply_fetcher_overrides(fetcher)


def apply_fetcher_overrides(fetcher):
    """Copy values from the appropriate override section into the root items"""
    global config
    overrides = config.get("overrides", {})

    if fetcher is None or fetcher.__module__ not in overrides.keys():
        return

    for key_1, val_1 in overrides[fetcher.__module__].items():
        if isinstance(val_1, dict):
            for key_2, val_2 in val_1.items():
                config[key_1][key_2] = val_2
        else:
            config[key_1] = val_1


def get(key):
    global config
    if isinstance(key, str):
        return config.get(key)
    elif isinstance(key, list):
        # chain of nested config items
        return functools.reduce(dict.__getitem__, key, config)


def get_fetcher_opt(key, required=False):
    fetcher_opts = config.get("fetcher_opts")
    if fetcher_opts:
        matching_opts = [opt for opt in fetcher_opts if opt.startswith(f"{key}=")]

        if matching_opts:
            # the last one "wins"
            return matching_opts[-1].split("=")[-1]

    if required:
        raise MissingRequiredFetcherOptError(key)
