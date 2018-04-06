class Constants(object):
    DEBUG = False

    PROJECT_NAME = 'EzoRed'

    PROJECT_FILE = 'ezored_project.yml'
    TARGET_DATA_FILE = 'ezored_target_data.yml'
    SOURCE_DIR = 'source'

    TARGET_MODULE_NAME = 'ezored_target'
    VENDOR_MODULE_NAME = 'ezored_vendor'

    ENV_VAR_PREFIX = 'EZORED_'

    DEPENDENCIES_DIR = 'vendor'
    TARGET_DIR = 'target'
    VENDOR_DIR = 'vendor'
    TEMP_DIR = 'temp'
    BUILD_DIR = 'build'

    GITHUB_DOWNLOAD_EXTENSION = 'tar.gz'

    PROJECT_FILE_DATA = """
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
      path: ezored/target-ios
      type: github
      version: b:master
  - name: android
    repository:
      path: ezored/target-android
      type: github
      version: b:master
dependencies:
  - name: djinni-support
    repository:
      path: ezored/dependency-djinni-support
      type: github
      version: b:master
  - name: sample
    repository:
      path: ezored/dependency-sample
      type: github
      version: b:master
"""
