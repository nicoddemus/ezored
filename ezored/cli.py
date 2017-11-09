"""
EzoRed

Usage:
  ezored dependencies update
  ezored hello
  ezored -h | --help
  ezored --version

Options:
  -h --help                         Show this screen.
  --version                         Show version.

Examples:
  ezored dependencies update

Help:
  For help using this tool, please open an issue on the Github repository:
  https://github.com/ezored/ezored
"""

from inspect import getmembers, isclass
from json import dumps

import ezored.commands
from docopt import docopt

from . import __version__


def main():
    """Main CLI entrypoint."""
    options = docopt(__doc__, version=__version__)

    print('You supplied the following options: ', dumps(options, indent=2, sort_keys=False))

    # Here we'll try to dynamically match the command the user is trying to run
    # with a pre-defined command class we've already created.
    for (k, v) in options.items():
        if hasattr(ezored.commands, k) and v:
            module = getattr(ezored.commands, k)
            ezored.commands = getmembers(module, isclass)
            command = [command[1] for command in ezored.commands if command[0] != 'Base'][0]
            command = command(options)
            command.run()
