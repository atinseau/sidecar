
from threading import Thread
from subprocess import PIPE, Popen

import psutil
import os

from .declare import Command


class Reader(Thread):
	def __init__(self, process_conf, global_conf):
		super().__init__(name=process_conf["name"] + "_" + process_conf["std"])

		self.process = process_conf["process"]
		self.process_name = process_conf["name"]
		self.std = process_conf["std"]
		self.stop = process_conf["stop"]
		self.command = process_conf["command"]

		self.global_conf = global_conf

	def __getline__(self, line):
		return "[{}] {}".format(self.process_name, line.decode("utf-8"))

	def run(self):
		while True and not self.stop:
			line: bytes = self.process.__getattribute__(self.std).readline()
			if not line:
				break
			if not self.stop and not self.global_conf["paused"]:
				if self.std == "stdout":
					print(self.__getline__(line), end="")
				else:
					stderr = self.command.get("stderr", None)
					if stderr is None or stderr is True:
						print(self.__getline__(line), end="")
					else:
						filename = stderr
						os.makedirs(os.path.dirname(filename), exist_ok=True)
						with open(filename, "a") as f:
							f.write(self.__getline__(line))


class Process (Thread):

	def __init__(self, command: Command, conf):
		super().__init__(name=command["name"])

		self.global_conf = conf
		self.command = command
		self.stop = False

	def kill(self):
		process = psutil.Process(self.process.pid)
		for proc in process.children(recursive=True):
			proc.kill()
		process.kill()
		self.stop = True

	def __launch__(self):
		self.process = Popen(
			[self.command["command"]],
			shell=True,
			preexec_fn=lambda: os.setpgrp(),
			stdout=PIPE,
			stderr=PIPE,
			close_fds=True
		)

	def __create_reader__(self, std):
		reader = Reader({
			"process": self.process,
			"stop": self.stop,
			"name": self.name,
			"std": std,
			"command": self.command
		}, self.global_conf)
		reader.start()
		return reader

	def run(self):
		self.__launch__()

		readers = [
			self.__create_reader__("stdout")
		]

		stderr = self.command.get("stderr")
		if stderr is not False or stderr is None :
			self.__create_reader__("stderr")
		
		for reader in readers:
			reader.join()
		print("[{}] Process finished".format(self.name))
