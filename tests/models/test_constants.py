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
  name: ezored
  ios:
    cmake_version: 3.9
    bundle_id: com.ezored.library
    version: 1.0.0
    cpp_standard: 11
    development_team_id: ABCDEFGHIJ
    code_sign_identity: iPhone Developer
    deployment_target: 8.0
    device_family: 1,2
    archs:
      - iphoneos
      - iphonesimulator
  android:
    cmake_version: 3.4.1
    bundle_id: com.ezored.library
    version: 1.0.0
    version_code: 1
    version_name: 1.0.0
    cpp_standard: 11
    gradle_plugin: 3.1.1
    compile_sdk_version: 27
    build_tools_version: 27.0.3
    min_sdk_version: 15
    target_sdk_version: 26
    support_lib_version: 27.1.1
    dependencies:
      - type: implementation
        path: com.android.support:appcompat-v7:${project.ext.supportLibVersion}
targets:
  - name: ios
    repository:
      path: ezored/target-ios
      type: git
      version: b:master
  - name: android
    repository:
      path: ezored/target-android
      type: git
      version: b:master
dependencies:
  - name: djinni-support
    repository:
      path: ezored/dependency-djinni-support
      type: git
      version: b:master
  - name: sample
    repository:
      path: ezored/dependency-sample
      type: git
      version: b:master
"""
        self.assertEqual(Constants.PROJECT_FILE_DATA, file_data)
