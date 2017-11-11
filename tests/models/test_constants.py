from unittest import TestCase

from ezored.models.constants import Constants


class TestConstants(TestCase):
    def test_initial_data(self):
        self.assertTrue(Constants.DEBUG == False)

    def test_project_file(self):
        self.assertTrue(Constants.PROJECT_FILE == "ezored-project.yml")

    def test_project_file_data(self):
        file_data = """
config:
  name: EzoRed
  ios:
    developmentTeamId: ABCDEFGHIJ
    bundleId: com.ezored.library
    codeSignIdentity: iPhone Developer
    deploymentTarget: '8.0'
    deviceFamily: '1,2'
    version: 1.0.0
    cppStandard: '11'
  android:
    cppStandard: '11'
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
- name: ezored/dependency-djinni-support
  type: github
  version: b:master
- name: ezored/dependency-sample
  type: github
  version: b:master
"""
        self.assertTrue(Constants.PROJECT_FILE_DATA == file_data)
