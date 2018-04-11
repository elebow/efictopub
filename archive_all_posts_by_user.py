#!/usr/bin/python3

import praw


class Main:
	def __init__(self, *, app, secret, user_agent, target):
		self.reddit = praw.Reddit(client_id=app, client_secret=secret, user_agent=user_agent)
		self.target = target
		import ipdb; ipdb.set_trace()


if __name__ == "__main__":
	import configparser
	import sys

	cfg = configparser.ConfigParser()
	cfg.read(sys.argv[1])
	app		= cfg.get('DEFAULT', 'app')
	secret   = cfg.get('DEFAULT', 'secret')
	user_agent = cfg.get("DEFAULT", "user_agent")

	Main(app=app, secret=secret, user_agent=user_agent, target=sys.argv[2]).export_all
