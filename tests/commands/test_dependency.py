import os
from subprocess import PIPE, Popen as popen
from unittest import TestCase

from ezored.models.constants import Constants
from testfixtures import tempdir


class TestDependency(TestCase):
    @tempdir()
    def test_dependency_list(self, d):
        os.chdir(d.path)

        d.write(Constants.PROJECT_FILE, Constants.PROJECT_FILE_DATA)

        required = """Dependency List:
  - ezored/dependency-djinni-support
  - ezored/dependency-sample
"""

        output = popen(['ezored', 'dependency', 'list'], stdout=PIPE).communicate()[0]
        self.assertTrue(output == required)
