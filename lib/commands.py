import json
import signal
import threading

from .process import Process
from .declare import Command
from .utils import responseOutput


class Commands:
	def __init__(self):
		signal.signal(signal.SIGINT, self.handler)
		self.threads: list[Process] = []
		self.conf = {
			"paused": False
		}
	
	def register(self, command: Command):
		thread = Process(command, self.conf)
		self.threads.append(thread)

	def start(self):
		[thread.start() for thread in self.threads]
		for thread in self.threads:
			thread.join()

	def handler(self, signum, frame):
		if self.conf["paused"]:
			return
		self.conf["paused"] = True
		code = responseOutput("\nAre you sure you want to stop the processses?")
		if code:
			for thread in self.threads:
				thread.kill()
		self.conf["paused"] = not self.conf["paused"]


def getCommands(path: str):
	try:
		with open(path) as f:
			config = json.load(f)
			commands: list[Command] = config["commands"]
			if commands.__len__() == 0:
				raise Exception("No commands found in config file")
			return commands
	except FileNotFoundError:
		print("Config file not found at \"{}\"".format(path))
	except Exception as e:
		print(e)
	return []