# Project

Ezored project file contains one or more targets inside, that you can build using the ezored from command-line.
 
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
```

### Thoubleshoots

- Use only valid chars on everything property that is a "name". Dont start the name with numbers. The rules are:  
`[a-z][A-Z][0-9]-_`. 

### Documentation Index

- [Back to index](GET-STARTED.md)
