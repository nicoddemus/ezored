import os
from subprocess import PIPE, Popen as popen
from unittest import TestCase

from ezored.models.constants import Constants
from testfixtures import tempdir


class TestDependency(TestCase):
    @tempdir()
    def test_dependency_list(self, d):
        os.chdir(d.path)

        d.write(Constants.PROJECT_FILE, Constants.PROJECT_FILE_DATA.encode('utf-8'))

        output = popen(['ezored', 'dependency', 'list'], stdout=PIPE).communicate()[0]
        output = str(output)

        required = 'Dependency List:'
        self.assertTrue(required in output)

        required = '- ezored/dependency-djinni-support'
        self.assertTrue(required in output)

        required = '- ezored/dependency-sample'
        self.assertTrue(required in output)
