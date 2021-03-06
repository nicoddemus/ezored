import os
from subprocess import PIPE, Popen as popen
from unittest import TestCase

from testfixtures import tempdir

from ezored.models.constants import Constants
from ezored.models.util.file_util import FileUtil


class TestTarget(TestCase):
    @tempdir()
    def test_target_list(self, d):
        os.chdir(d.path)

        d.write(Constants.PROJECT_FILE, Constants.PROJECT_FILE_DATA.encode('utf-8'))

        output = popen(['ezored', 'target', 'list'], stdout=PIPE).communicate()[0]
        output = str(output)
        print(output)

        required = 'Target List:'
        self.assertTrue(required in output)

        required = '- ios'
        self.assertTrue(required in output)

        required = '- android'
        self.assertTrue(required in output)

    @tempdir()
    def test_target_git_build_all(self, d):
        os.chdir(d.path)

        project_file_data = """
config:
  name: ezored
targets:
  - name: git-test
    repository:
      path: https://github.com/ezored/target-git-test.git
      type: git
      version: b:master
dependencies:
  - name: git-test
    repository:
      path: https://github.com/ezored/dependency-git-test.git
      type: git
      version: b:master      
"""

        d.write(Constants.PROJECT_FILE, project_file_data.encode('utf-8'))

        output = popen(['ezored', 'dependency', 'install', '-d'], stdout=PIPE).communicate()[0]
        output = str(output)
        print(output)

        output = popen(['ezored', 'target', 'build', '-d'], stdout=PIPE).communicate()[0]
        output = str(output)
        print(output)

        required = 'Command "build" finished for target "git-test"'
        self.assertTrue(required in output)

        self.assertTrue(os.path.exists(os.path.join('vendor', 'target-git-test', 'file-to-parse.txt')))
        self.assertTrue(os.path.exists(os.path.join('vendor', 'target-git-test', 'ezored_target.py')))
        self.assertTrue(os.path.exists(os.path.join('vendor', 'target-git-test', 'ezored_target_data.yml')))

    @tempdir()
    def test_target_git_build_single(self, d):
        os.chdir(d.path)

        project_file_data = """
config:
  name: ezored
targets:
  - name: git-test 
    repository:
      path: https://github.com/ezored/target-git-test.git
      type: git
      version: b:master
dependencies:
  - name: git-test
    repository:
      path: https://github.com/ezored/dependency-git-test.git
      type: git
      version: b:master      
"""

        d.write(Constants.PROJECT_FILE, project_file_data.encode('utf-8'))

        output = popen(['ezored', 'dependency', 'install', '-d'], stdout=PIPE).communicate()[0]
        output = str(output)
        print(output)

        output = popen(['ezored', 'target', 'build', 'git-test', '-d'], stdout=PIPE).communicate()[0]
        output = str(output)
        print(output)

        required = 'Command "build" finished for target "git-test"'
        self.assertTrue(required in output)

        self.assertTrue(os.path.exists(os.path.join('vendor', 'target-git-test', 'file-to-parse.txt')))
        self.assertTrue(os.path.exists(os.path.join('vendor', 'target-git-test', 'ezored_target.py')))
        self.assertTrue(os.path.exists(os.path.join('vendor', 'target-git-test', 'ezored_target_data.yml')))

    @tempdir()
    def test_target_git_copy_file(self, d):
        os.chdir(d.path)

        project_file_data = """
config:
  name: ezored
targets:
  - name: git-test 
    repository:
      path: https://github.com/ezored/target-git-test.git
      type: git
      version: b:master
dependencies:
  - name: git-test
    repository:
      path: https://github.com/ezored/dependency-git-test.git
      type: git
      version: b:master      
"""

        d.write(Constants.PROJECT_FILE, project_file_data.encode('utf-8'))

        output = popen(['ezored', 'dependency', 'install', '-d'], stdout=PIPE).communicate()[0]
        output = str(output)
        print(output)

        output = popen(['ezored', 'target', 'build', 'git-test', '-d'], stdout=PIPE).communicate()[0]
        output = str(output)
        print(output)

        required = 'Command "build" finished for target "git-test"'
        self.assertTrue(required in output)

        self.assertTrue(os.path.exists(os.path.join('vendor', 'target-git-test', 'file-to-parse.txt')))
        self.assertTrue(os.path.exists(os.path.join('vendor', 'target-git-test', 'ezored_target.py')))
        self.assertTrue(os.path.exists(os.path.join('vendor', 'target-git-test', 'ezored_target_data.yml')))

        self.assertTrue(os.path.exists(os.path.join('vendor', 'target-git-test', 'source', 'test-copy.py')))

    @tempdir()
    def test_target_git_parse_file(self, d):
        os.chdir(d.path)

        project_file_data = """
config:
  name: ezored
targets:
  - name: git-test 
    repository:
      path: https://github.com/ezored/target-git-test.git
      type: git
      version: b:master
dependencies:
  - name: git-test
    repository:
      path: https://github.com/ezored/dependency-git-test.git
      type: git
      version: b:master      
"""

        d.write(Constants.PROJECT_FILE, project_file_data.encode('utf-8'))

        output = popen(['ezored', 'dependency', 'install', '-d'], stdout=PIPE).communicate()[0]
        output = str(output)
        print(output)

        output = popen(['ezored', 'target', 'build', 'git-test', '-d'], stdout=PIPE).communicate()[0]
        output = str(output)
        print(output)

        required = 'Command "build" finished for target "git-test"'
        self.assertTrue(required in output)

        file_to_read = os.path.join('vendor', 'target-git-test', 'file-to-parse.txt')
        self.assertTrue(os.path.exists(file_to_read))

        content = FileUtil.read_file(file_to_read)
        self.assertEqual(content, Constants.PROJECT_NAME)

    @tempdir()
    def test_no_targets(self, d):
        os.chdir(d.path)

        project_file_data = """
config:
  name: ezored
"""

        d.write(Constants.PROJECT_FILE, project_file_data.encode('utf-8'))

        output = popen(['ezored', 'target', 'build'], stdout=PIPE).communicate()[0]
        output = str(output)
        print(output)

        required = 'Your project does not have targets'
        self.assertTrue(required in output)

    @tempdir()
    def test_target_command_test(self, d):
        os.chdir(d.path)

        project_file_data = """
config:
  name: ezored
targets:
  - name: git-test 
    repository:
      path: https://github.com/ezored/target-git-test.git
      type: git
      version: b:master
"""

        d.write(Constants.PROJECT_FILE, project_file_data.encode('utf-8'))

        output = popen(['ezored', 'target', 'test', 'git-test', '-d'], stdout=PIPE).communicate()[0]
        output = str(output)
        print(output)

        required = 'Command "test" finished for target "git-test"'
        self.assertTrue(required in output)
