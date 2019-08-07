# Module to store config values read from the file

import confuse

# Config value precedence, from lowest to highest:
#   - The nested structure in the config file, except for `overrides`.
#   - Any values specified under `overrides` for the chosen fetcher
#   - Any values specified on the command line

# See https://confuse.readthedocs.io/en/latest/#search-paths for config file locations


def load(*, args, fetcher):
    global config
    config = load_config_file()

    apply_fetcher_overrides(config, fetcher)
    apply_cli_arg_overrides(config, args)


def load_config_file():
    return confuse.Configuration("efictopub", __name__)


def apply_fetcher_overrides(config, fetcher):
    """Copy values from the appropriate override section into the root items"""
    overrides = config["overrides"]

    if fetcher is None or fetcher.__module__ not in overrides.keys():
        return config

    for key_1, val_1 in overrides[fetcher.__module__].items():
        if isinstance(val_1, dict):
            for key_2, val_2 in val_1.items():
                config[key_1][key_2] = val_2.get()
        else:
            config[key_1] = val_1.get()

    return config


def apply_cli_arg_overrides(config, args):
    config.set_args(args, dots=True)


# Always load _something_, because other modules expect it
# This will be called a second time from Controller with the real values
load(args={}, fetcher=None)
