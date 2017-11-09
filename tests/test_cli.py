"""Tests for our main EzoRed CLI module."""

from subprocess import PIPE, Popen as popen
from unittest import TestCase

from ezored import __version__ as VERSION


class TestHelp(TestCase):
    def test_returns_usage_information(self):
        output = popen(['ezored', '-h'], stdout=PIPE).communicate()[0]
        self.assertTrue('Usage:' in output)

        output = popen(['ezored', '--help'], stdout=PIPE).communicate()[0]
        self.assertTrue('Usage:' in output)


class TestVersion(TestCase):
    def test_returns_version_information(self):
        output = popen(['ezored', '--version'], stdout=PIPE).communicate()[0]
        self.assertEqual(output.strip(), VERSION)
