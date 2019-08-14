#!python3

from efictopub import cli
from efictopub.controller import Controller


Controller(cli.args()).run()
