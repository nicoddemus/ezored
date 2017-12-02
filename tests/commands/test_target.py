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
      name: ${HOME}/Developer/workspaces/cpp/target-github-test
      type: local
"""

        d.write(Constants.PROJECT_FILE, project_file_data.encode('utf-8'))

        output = popen(['ezored', 'target', 'build'], stdout=PIPE).communicate()[0]
        output = str(output)

        required = 'Build finished for repository: target-github-test'
        self.assertTrue(required in output)

        self.assertTrue(os.path.exists(os.path.join('vendor', 'target-github-test', 'file-to-parse.txt')))
        self.assertTrue(os.path.exists(os.path.join('vendor', 'target-github-test', 'ezored-target.yml')))
        self.assertTrue(os.path.exists(os.path.join('vendor', 'target-github-test', 'build.py')))

    @tempdir()
    def test_target_github_build_single(self, d):
        os.chdir(d.path)

        project_file_data = """
config:
  name: EzoRed
targets:
  - name: github-test
    repository:
      name: ${HOME}/Developer/workspaces/cpp/target-github-test
      type: local
"""

        d.write(Constants.PROJECT_FILE, project_file_data.encode('utf-8'))

        output = popen(['ezored', 'target', 'build', 'github-test'], stdout=PIPE).communicate()[0]
        output = str(output)

        required = 'Build finished for repository: target-github-test'
        self.assertTrue(required in output)

        self.assertTrue(os.path.exists(os.path.join('vendor', 'target-github-test', 'file-to-parse.txt')))
        self.assertTrue(os.path.exists(os.path.join('vendor', 'target-github-test', 'ezored-target.yml')))
        self.assertTrue(os.path.exists(os.path.join('vendor', 'target-github-test', 'build.py')))
