import os
from ..commands import getCommands
from ..declare import Command, SidecarConf
from ..utils import responseOutput


def default(commands: list[Command]):
	for command in commands:
		stderr = command.get("stderr")
		if type(stderr) is str:
			print(f'------[{command["name"]}]------')
			try:
				with open(stderr, 'r') as f:
					print(f.read(), end='')
			except FileNotFoundError:
				print(f"Log file not found: {stderr}")


def clear(commands: list[Command], args: list[str] = []):

	force = False
	for arg in args:
		if arg == "--force":
			force = True

	for command in commands:
		if stderr := command.get("stderr"):
			try:
				if force or responseOutput(f"Are you sure you want to clear the log file: \"{stderr}\" ?"):
					os.remove(stderr)
					print(f"Log file removed: {stderr}")
			except FileNotFoundError:
				print(f"Log file not found: {stderr}")

def logs(conf: SidecarConf):
	commands = getCommands(conf["config_file"])
	if conf["args"].__len__() == 0:
		default(commands)
	elif conf["args"][0] == "clear":
		clear(commands, conf["args"][1:])
