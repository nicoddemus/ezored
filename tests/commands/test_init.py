import os
from subprocess import PIPE, Popen as popen
from unittest import TestCase

from testfixtures import tempdir

from ezored.models.constants import Constants


class TestInit(TestCase):
    @tempdir()
    def test_init(self, d):
        os.chdir(d.path)

        output = popen(['ezored', 'init'], stdout=PIPE).communicate()[0]
        output = str(output)
        print(output)

        required = 'A new ezored project was initialized with success'
        self.assertTrue(required in output)

    @tempdir()
    def test_init_with_project_file_already_exists(self, d):
        os.chdir(d.path)

        d.write(Constants.PROJECT_FILE, Constants.PROJECT_FILE_DATA.encode('utf-8'))

        output = popen(['ezored', 'init'], stdout=PIPE).communicate()[0]
        output = str(output)
        print(output)

        required = 'A new ezored project was initialized with success'
        self.assertTrue(required in output)
