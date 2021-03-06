"""
ezored

Usage:
  ezored [options] init
  ezored [options] dependency list
  ezored [options] dependency install
  ezored [options] dependency install <dependency-name>
  ezored [options] target list
  ezored [options] target <target-command>
  ezored [options] target <target-command> <target-name>
  ezored [options] clean
  ezored -h | --help

Options:
  -h --help                         Show this screen.
  --version                         Show version.
  -d --debug                        Enable debug messages.

Examples:
  ezored init
  ezored dependency list
  ezored dependency install
  ezored target list
  ezored target build
  ezored clean

Help:
  For help using this tool, please open an issue on the Github repository:
  https://github.com/ezored/ezored
"""
import os
import platform
from inspect import getmembers, isclass
from json import dumps

from docopt import docopt

import ezored.commands
from ezored.models.constants import Constants
from ezored.models.logger import Logger
from . import __version__


def main():
    """Main CLI entrypoint."""
    options = docopt(__doc__, version=__version__)

    # show all params for debug
    if ('--debug' in options and options['--debug']) or ('-d' in options and options['-d']):
        Constants.DEBUG = True
        Logger.clean('System information: ')
        Logger.clean('> Process id: {0}'.format(os.getpid()))
        Logger.clean('> Python: {0}'.format(platform.python_version()))
        Logger.clean('')
        Logger.clean('You supplied the following options: ')
        Logger.clean('{0}'.format(dumps(options, indent=2, sort_keys=False)))
        Logger.clean('')

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
