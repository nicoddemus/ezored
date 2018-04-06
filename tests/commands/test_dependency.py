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
        print(output)

        required = 'Dependency List:'
        self.assertTrue(required in output)

        required = '- djinni-support'
        self.assertTrue(required in output)

        required = '- sample'
        self.assertTrue(required in output)

    @tempdir()
    def test_dependency_github_update(self, d):
        os.chdir(d.path)

        project_file_data = """
config:
  name: EzoRed
dependencies:
  - name: github-test
    repository:
      path: ezored/dependency-github-test
      type: github
      version: b:master
"""

        d.write(Constants.PROJECT_FILE, project_file_data.encode('utf-8'))

        output = popen(['ezored', 'dependency', 'update'], stdout=PIPE).communicate()[0]
        output = str(output)
        print(output)

        required = 'Build finished for repository: ezored-dependency-github-test'
        self.assertTrue(required in output)

    @tempdir()
    def test_no_dependencies(self, d):
        os.chdir(d.path)

        project_file_data = """
config:
  name: EzoRed
"""

        d.write(Constants.PROJECT_FILE, project_file_data.encode('utf-8'))

        output = popen(['ezored', 'dependency', 'update'], stdout=PIPE).communicate()[0]
        output = str(output)
        print(output)

        required = 'Your project does not have dependencies'
        self.assertTrue(required in output)

    @tempdir()
    def test_dependency_single_update(self, d):
        os.chdir(d.path)

        project_file_data = """
config:
  name: EzoRed
dependencies:
  - name: github-test
    repository:
      path: ezored/dependency-github-test
      type: github
      version: b:master
"""

        d.write(Constants.PROJECT_FILE, project_file_data.encode('utf-8'))

        output = popen(['ezored', 'dependency', 'update', 'github-test'], stdout=PIPE).communicate()[0]
        output = str(output)
        print(output)

        required = 'Build finished for repository: ezored-dependency-github-test'
        self.assertTrue(required in output)

    @tempdir()
    def test_dependency_single_update_invalid(self, d):
        os.chdir(d.path)

        project_file_data = """
config:
  name: EzoRed
dependencies:
  - name: github-test
    repository:
      path: ezored/dependency-github-test
      type: github
      version: b:master
"""

        d.write(Constants.PROJECT_FILE, project_file_data.encode('utf-8'))

        output = popen(['ezored', 'dependency', 'update', 'test-invalid'], stdout=PIPE).communicate()[0]
        output = str(output)
        print(output)

        required = 'Dependency not found: test-invalid'
        self.assertTrue(required in output)
