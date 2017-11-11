from subprocess import PIPE, Popen as popen
from unittest import TestCase

from ezored import __version__ as VERSION


class TestCLI(TestCase):
    def test_returns_usage_information(self):
        output = popen(['ezored', '-h'], stdout=PIPE).communicate()[0]
        output = str(output)

        self.assertTrue('Usage:' in output)

        output = popen(['ezored', '--help'], stdout=PIPE).communicate()[0]
        output = str(output)

        self.assertTrue('Usage:' in output)

    def test_returns_version_information(self):
        output = popen(['ezored', '--version'], stdout=PIPE).communicate()[0]
        output = str(output)

        self.assertTrue(VERSION in output)

    def test_debug(self):
        required = 'DEBUG: You supplied the following options:'

        output = popen(['ezored', '--debug'], stdout=PIPE).communicate()[0]
        output = str(output)

        self.assertTrue(required in output)
