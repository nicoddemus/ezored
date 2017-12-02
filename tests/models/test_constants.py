from unittest import TestCase

from ezored.models.constants import Constants


class TestConstants(TestCase):
    def test_initial_data(self):
        self.assertEqual(Constants.DEBUG, False)

    def test_project_file(self):
        self.assertEqual(Constants.PROJECT_FILE, 'ezored-project.yml')

    def test_project_file_data(self):
        file_data = """
config:
  name: EzoRed
  ios:
    development_team_id: ABCDEFGHIJ
    bundle_id: com.ezored.library
    code_sign_identity: iPhone Developer
    deployment_target: '8.0'
    device_family: '1,2'
    version: 1.0.0
    cpp_standard: '11'
  android:
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
  - name: dependency-djinni-support
    repository:
      name: ezored/dependency-djinni-support
      type: github
      version: b:master
  - name: dependency-sample
    repository:
      name: ezored/dependency-sample
      type: github
      version: b:master
"""
        self.assertEqual(Constants.PROJECT_FILE_DATA, file_data)
