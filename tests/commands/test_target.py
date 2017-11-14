import os
from subprocess import PIPE, Popen as popen
from unittest import TestCase

from ezored.models.constants import Constants
from testfixtures import tempdir


class TestTarget(TestCase):
    @tempdir()
    def test_target_list(self, d):
        os.chdir(d.path)

        d.write(Constants.PROJECT_FILE, Constants.PROJECT_FILE_DATA.encode('utf-8'))

        output = popen(['ezored', 'target', 'list'], stdout=PIPE).communicate()[0]
        output = str(output)

        required = 'Target List:'
        self.assertTrue(required in output)

        required = '- ios'
        self.assertTrue(required in output)

        required = '- android'
        self.assertTrue(required in output)
