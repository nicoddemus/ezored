"""
EzoRed

Usage:
  ezored dependency list [-d]
  ezored dependency update [-d]
  ezored target list [-d]
  ezored hello
  ezored -h | --help
  ezored [-d | --debug]

Options:
  -h --help                         Show this screen.
  --version                         Show version.
  -d --debug                        Enable debug messages.

Examples:
  ezored dependency list
  ezored target list -d

Help:
  For help using this tool, please open an issue on the Github repository:
  https://github.com/ezored/ezored
"""

from inspect import getmembers, isclass
from json import dumps

import ezored.commands
from docopt import docopt
from models.constants import Constants
from models.logger import Logger

from . import __version__


def main():
    """Main CLI entrypoint."""
    options = docopt(__doc__, version=__version__)

    # show all params for debug
    if ("--debug" in options and options["--debug"]) or ("-d" in options and options["-d"]):
        Constants.DEBUG = True
        Logger.d('You supplied the following options: ')
        Logger.d("\n{0}".format(dumps(options, indent=2, sort_keys=False)))
        Logger.clean("")

    # dynamically match the command that user is trying to run
    for (option_key, option_value) in options.items():
        if hasattr(ezored.commands, option_key) and option_value:
            command_module = getattr(ezored.commands, option_key)
            commands = getmembers(command_module, isclass)

            ezcommand = None

            for command in commands:
                if command[0] != 'Base' and command[0].lower() == option_key:
                    ezcommand = command[1](options)
                    break

            if ezcommand:
                ezcommand.run()
