class Constants(object):
    DEBUG = False

    PROJECT_NAME = 'EzoRed'

    PROJECT_FILE = 'ezored-project.yml'
    VENDOR_FILE = 'ezored-vendor.yml'
    TARGET_FILE = 'ezored-target.yml'
    TARGET_PROJECT_FILE = 'ezored-target.yml'
    SOURCE_DIR = 'source'

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
  - repository:
      name: ezored/dependency-djinni-support
      type: github
      version: b:master
  - repository:
      name: ezored/dependency-sample
      type: github
      version: b:master
"""
