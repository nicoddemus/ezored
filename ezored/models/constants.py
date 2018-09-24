class Constants(object):
    DEBUG = False

    PROJECT_NAME = 'ezored'

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

    REPOSITORY_TYPE_LOCAL = 'local'
    REPOSITORY_TYPE_GIT = 'git'
    REPOSITORY_TYPE_ZIP = 'zip'
    REPOSITORY_TYPE_TAR = 'tar'

    GIT_TYPE_BRANCH = 'b'
    GIT_TYPE_TAG = 't'
    GIT_TYPE_COMMIT = 'c'

    PROJECT_FILE_DATA = """
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
      version: t:1.0.0
"""
