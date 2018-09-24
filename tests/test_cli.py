import os
from subprocess import PIPE, Popen as popen
from unittest import TestCase

from testfixtures import tempdir

from ezored import __version__ as VERSION
from ezored.models.constants import Constants


class TestCLI(TestCase):
    def test_returns_usage_information(self):
        output = popen(['ezored', '-h'], stdout=PIPE).communicate()[0]
        output = str(output)
        print(output)

        self.assertTrue('Usage:' in output)

        output = popen(['ezored', '--help'], stdout=PIPE).communicate()[0]
        output = str(output)
        print(output)

        self.assertTrue('Usage:' in output)

    def test_returns_version_information(self):
        output = popen(['ezored', '--version'], stdout=PIPE).communicate()[0]
        output = str(output)
        print(output)

        self.assertTrue(VERSION in output)

    @tempdir()
    def test_debug(self, d):
        os.chdir(d.path)
        d.write(Constants.PROJECT_FILE, Constants.PROJECT_FILE_DATA.encode('utf-8'))

        required = 'DEBUG: You supplied the following options:'

        output = popen(['ezored', 'init', '--debug'], stdout=PIPE).communicate()[0]
        output = str(output)
        print(output)

        self.assertTrue(required in output)
