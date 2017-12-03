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

    @tempdir()
    def test_target_github_build_all(self, d):
        os.chdir(d.path)

        project_file_data = """
config:
  name: EzoRed
targets:
  - name: github-test
    repository:
      name: ezored/target-github-test
      type: github
      version: b:master
"""

        d.write(Constants.PROJECT_FILE, project_file_data.encode('utf-8'))

        output = popen(['ezored', 'target', 'build', '-d'], stdout=PIPE).communicate()[0]
        output = str(output)
        print(output)

        required = 'Build finished for target: github-test'
        self.assertTrue(required in output)

        self.assertTrue(os.path.exists(os.path.join('vendor', 'target-github-test-master', 'file-to-parse.txt')))
        self.assertTrue(os.path.exists(os.path.join('vendor', 'target-github-test-master', 'ezored-target.yml')))
        self.assertTrue(os.path.exists(os.path.join('vendor', 'target-github-test-master', 'build.py')))

    @tempdir()
    def test_target_github_build_single(self, d):
        os.chdir(d.path)

        project_file_data = """
config:
  name: EzoRed
targets:
  - name: github-test 
    repository:
      name: ezored/target-github-test
      type: github
      version: b:master
"""

        d.write(Constants.PROJECT_FILE, project_file_data.encode('utf-8'))

        output = popen(['ezored', 'target', 'build', 'github-test', '-d'], stdout=PIPE).communicate()[0]
        output = str(output)
        print(output)

        required = 'Build finished for target: github-test'
        self.assertTrue(required in output)

        self.assertTrue(os.path.exists(os.path.join('vendor', 'target-github-test-master', 'file-to-parse.txt')))
        self.assertTrue(os.path.exists(os.path.join('vendor', 'target-github-test-master', 'ezored-target.yml')))
        self.assertTrue(os.path.exists(os.path.join('vendor', 'target-github-test-master', 'build.py')))
