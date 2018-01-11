# Targets

A target consists in a bunch of files that need exists to build a project. The target files can be parsed, like `CMakeLists.txt`.   

The target project has all dependencies files, params, libraries, links and other things ready to build and compile.    

### Target block structure

The target block structure has this properties:
- name
- repository  
  - type
  - name
  - version
- tasks  

The property `"repository.type"` define how EzoRed will get your target. Today we support types:
- local  
- github  

The property `"repository.name"` define how EzoRed will find your target based on `"type"`. Example:  
- `local` = You need set the path to the target directory, ex: `${HOME}/my-target`  
- `github` = You need set the repository name, ex: `ezored/target-android` 

The property `"repository.version"` define what version EzoRed need download, ex: `"1.2.0"`. Git repositories have some especial version parse rules:
- `b:master` = will download version from branch "master" 
- `t:1.2.0` = will download version from tag "1.2.0" 
- `c:ef016c0` = will download version from commit "ef016c0" 
- `1.2.0` = without prefix will download version from tag "1.2.0" 
- `empty` = empty version field will download version from branch master 

The property `"tasks"` contains a list of Tasks. This tasks are merged on build process with all dependencies tasks and executed before build command be executed. 

### Custom targets

You can use official targets or you can copy one official and change it or build your own target from scratch. You only need configure a new block of target inside project file and make it local to test the target while you develop it.    

One simple example is about Android and Gradle dependencies. Today we have a simple `build.gradle` file, but if your target have more dependencies with custom repositories and other things, you can clone our android target and change it to reach your needs.

### Example

Some target examples:

```yaml
targets:
  - name: ios
    repository:
      name: ezored/target-ios
      type: github
      version: b:master
```

```yaml
targets:
  - name: android
    repository:
      name: "${HOME}/Developer/target-android"
      type: local
``` 

### Documentation Index

- [Back to index](GET-STARTED.md)
