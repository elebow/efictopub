#!python3

from app import config_loader
from app import cli
from app.controller import Controller


Controller(cli.args()).run()
