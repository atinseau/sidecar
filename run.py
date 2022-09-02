#!/usr/bin/python3

import sys

from launcher import execute
from lib.declare import SidecarConf


paused = False


if __name__ == "__main__":
	conf: SidecarConf = {
		"config_file": None,
		"command": None,
		"args": []
	}
	for argv in sys.argv[1:]:
		if argv.find("=") > 0:
			args = argv.split("=")
			if args[0] == "--path" or args[0] == "-p":
				conf["config_file"] = args[1]
		elif argv == "--help" or argv == "-h":
			conf["args"].append(argv)
		else:
			if conf["command"] is None:
				conf["command"] = argv
			else:
				conf["args"].append(argv)
	if conf["config_file"] is None:
		print("No config file specified")
		sys.exit(1) 
	execute(conf)
	
	