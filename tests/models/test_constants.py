from unittest import TestCase

from ezored.models.constants import Constants


class TestConstants(TestCase):
    def test_initial_data(self):
        self.assertEqual(Constants.DEBUG, False)

    def test_project_file(self):
        self.assertEqual(Constants.PROJECT_FILE, 'ezored_project.yml')

    def test_project_file_data(self):
        file_data = """
config:
  name: EzoRed
  ios:
    cmake_version: 3.9
    development_team_id: ABCDEFGHIJ
    bundle_id: com.ezored.library
    code_sign_identity: iPhone Developer
    deployment_target: '8.0'
    device_family: '1,2'
    version: 1.0.0
    cpp_standard: '11'
  android:
    cmake_version: 3.4.1
    cpp_standard: '11'
targets:
  - name: ios
    repository:
      name: ezored/target-ios
      type: github
      version: b:master
  - name: android
    repository:
      name: ezored/target-android
      type: github
      version: b:master
dependencies:
  - repository:
      name: ezored/dependency-djinni-support
      type: github
      version: b:master
  - repository:
      name: ezored/dependency-sample
      type: github
      version: b:master
"""
        self.assertEqual(Constants.PROJECT_FILE_DATA, file_data)
