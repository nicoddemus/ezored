import os
from subprocess import PIPE, Popen as popen
from unittest import TestCase

from testfixtures import tempdir

from ezored.models.constants import Constants


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
    def test_dependency_git_update(self, d):
        os.chdir(d.path)

        project_file_data = """
config:
  name: ezored
dependencies:
  - name: git-test
    repository:
      path: https://github.com/ezored/dependency-git-test.git
      type: git
      version: b:master
"""

        d.write(Constants.PROJECT_FILE, project_file_data.encode('utf-8'))

        output = popen(['ezored', 'dependency', 'update'], stdout=PIPE).communicate()[0]
        output = str(output)
        print(output)

        required = 'Build finished for repository: ezored-dependency-git-test'
        self.assertTrue(required in output)

    @tempdir()
    def test_no_dependencies(self, d):
        os.chdir(d.path)

        project_file_data = """
config:
  name: ezored
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
  name: ezored
dependencies:
  - name: git-test
    repository:
      path: https://github.com/ezored/dependency-git-test.git
      type: git
      version: b:master
"""

        d.write(Constants.PROJECT_FILE, project_file_data.encode('utf-8'))

        output = popen(['ezored', 'dependency', 'update', 'git-test'], stdout=PIPE).communicate()[0]
        output = str(output)
        print(output)

        required = 'Build finished for repository: ezored-dependency-git-test'
        self.assertTrue(required in output)

    @tempdir()
    def test_dependency_single_update_invalid(self, d):
        os.chdir(d.path)

        project_file_data = """
config:
  name: ezored
dependencies:
  - name: git-test
    repository:
      path: https://github.com/ezored/dependency-git-test.git
      type: git
      version: b:master
"""

        d.write(Constants.PROJECT_FILE, project_file_data.encode('utf-8'))

        output = popen(['ezored', 'dependency', 'update', 'test-invalid'], stdout=PIPE).communicate()[0]
        output = str(output)
        print(output)

        required = 'Dependency not found: test-invalid'
        self.assertTrue(required in output)
