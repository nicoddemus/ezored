# Project

EzoRed project file contains one or more targets inside, that you can build using the EzoRed from command-line.
 
The final target project generally is a library that have all native code compiled for the target specific platform.

To build each target inside EzoRed project file, we use a bunch of rules, including target project and all project dependencies rules.

### Project file

The project consists in a single file called "ezored-project.json".  

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

A sample EzoRed project file:

```yaml
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
```

### Thoubleshoots

- Use only valid chars on config "name" `[a-z][A-Z][0-9]-_`. Dont start the name with numbers.

### Documentation Index

- [Back to index](GET-STARTED.md)
