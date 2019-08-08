#!python3

from app import cli
from app.controller import Controller


Controller(cli.args()).run()
