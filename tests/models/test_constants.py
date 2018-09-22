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
    bundle_id: com.ezored.library
    version: 1.0.0
    development_team_id: ABCDEFGHIJ    
  android:
    bundle_id: com.ezored.library
    version: 1.0.0
    version_code: 1
    use_ndk_unified_headers: true
    dependencies:
      - type: implementation
        path: com.android.support:appcompat-v7:${project.ext.supportLibVersion}
  macos:
    type: framework
  linux:
    type: shared-lib
  windows:
    type: shared-lib
targets:
  - name: ios
    repository:
      path: https://github.com/ezored/target-ios.git
      type: git
      version: b:master
  - name: android
    repository:
      path: https://github.com/ezored/target-android.git
      type: git
      version: b:master
  - name: linux
    repository:
      path: https://github.com/ezored/target-linux.git
      type: git
      version: b:master
  - name: windows
    repository:
      path: https://github.com/ezored/target-windows.git
      type: git
      version: b:master
  - name: macos
    repository:
      path: https://github.com/ezored/target-macos.git
      type: git
      version: b:master
dependencies:
  - name: djinni-support
    repository:
      path: https://github.com/ezored/dependency-djinni-support.git
      type: git
      version: t:1.0.1
  - name: sample
    repository:
      path: https://github.com/ezored/dependency-sample.git
      type: git
      version: b:master
"""

        self.assertEqual(Constants.PROJECT_FILE_DATA, file_data)
