
import os
from lib import \
	Commands, \
	SidecarConf, \
	getCommands, \
	logs


def exec_commands(conf: SidecarConf):
	loader = Commands()
	commands = getCommands(conf["config_file"])
	for command in commands:
		loader.register(command)
	loader.start()


def execute(conf: SidecarConf):
	if conf["command"] is None:
		for arg in conf["args"]:
			if arg == "--help":
				with open("README.md", "r") as f:
					os.system('clear')
					print(f"{f.read()}", end="")
					return

		exec_commands(conf)
	elif conf["command"] == "logs":
		logs(conf)