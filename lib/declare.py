from typing import Optional, TypedDict

Command = TypedDict("Command", {
	"name": str,
	"command": str,
	"stderr": Optional[str]
})

SidecarConf = TypedDict("SidecarConf", {
	"config_file": str,
	"command": Optional[str],
	"args": list[str]
})
