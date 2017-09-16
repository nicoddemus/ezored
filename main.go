package main

import (
	"flag"
	"github.com/ezored/ezored/commands"
)

const (
	COMMAND_HELP         = "help"
	COMMAND_INIT         = "init"
	COMMAND_CLEAN        = "clean"
	COMMAND_DEPENDENCIES = "dependencies"
	COMMAND_BUILD        = "build"
)

func main() {
	// parse command flags
	flag.Parse()

	if len(flag.Args()) == 0 {
		showHelp()
		return
	}

	command := flag.Arg(0)

	// check executed command
	switch command {
	case COMMAND_HELP:
		showHelp()
		break
	case COMMAND_INIT:
		command := &commands.InitCommand{}
		command.Init()
		break
	case COMMAND_CLEAN:
		command := &commands.CleanCommand{}
		command.Init()
		break
	case COMMAND_DEPENDENCIES:
		command := &commands.DependenciesCommand{}
		command.Init()
		break
	case COMMAND_BUILD:
		command := &commands.BuildCommand{}
		command.Init()
		break
	default:
		showHelp()
	}
}

func showHelp() {
	command := &commands.HelpCommand{}
	command.Init()
}
