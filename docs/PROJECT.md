# Project

A project file of ezored contains one or more targets inside, that you can build using the ezored from command-line.
 
The final target project generally is a library that have all native code compiled for the target specific platform.

To build each target inside ezored project file, we use a bunch of rules, including target project and all project dependencies rules.

### Project file

The project consists in a single file called "ezored_project.yml".  

The project file have this properties:  

- config
- targets
- dependencies

The property `"config"` has project configurations, like name, version, bundle ID and other things.

The property `"targets"` has target list with their location to be downloaded. Can be an official target or your custom target project.

The property `"dependencies"` has all project dependencies, that will be downloaded and stored inside `"vendor"` folder.

Today we have implemented officially this targets:

- ios
- android

### Sample

A sample ezored project file:

```yaml
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
```

### Thoubleshoots

- Use only valid chars on everything property that is a "name". Dont start the name with numbers. The rules are:  
`[a-z][A-Z][0-9]-_`. 

### Documentation Index

- [Back to index](GET-STARTED.md)
