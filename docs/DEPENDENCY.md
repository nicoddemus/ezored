# Dependencies

A dependency consists in a small part of software, like a HTTP library, ZIP library, openssl, curl or your custom business code, that will be reused by your other projects.

Each dependency block has a supported repository inside.    

### Dependency block structure

The dependency block structure has this properties:  

- repository  
  - type
  - name
  - version
- tasks  

The property in `"repository.type"` define how ezored will get your dependency. Today we support types:
- local  
- github  

The property `"repository.name"` define how ezored will find your dependency based on `"type"`. Example:  
- `local` = You need set the path to the dependency directory, ex: `${HOME}/my-dependency`  
- `github` = You need set the repository name, ex: `ezored/dependency-sample` 

The property `"repository.version"` define what version ezored need download, ex: `"1.2.0"`. Git repositories have some especial version parse rules:
- `b:master` = will download version from branch "master" 
- `t:1.2.0` = will download version from tag "1.2.0" 
- `c:ef016c0` = will download version from commit "ef016c0" 
- `1.2.0` = without prefix will download version from tag "1.2.0" 
- `empty` = empty version field will download version from branch master 

The property `"tasks"` contains a list of Tasks. This tasks are merged on build process with target tasks and executed before the target build command be executed.

### Custom dependencies

You can use official dependencies or you can copy one official and change it or build your own dependency from scratch. You only need configure a new block of dependency inside project file and make it local to test the dependency while you develop it.    

One simple example is about your business logic. You can use a local dependency with your business logic in a private path or repository, develop your app and change or debug the dependency code at the same time. The only restriction is when you add new files to dependency project, you will need run `"ezored target build <target-name>"` to update target project with new files. 

### Example

Some dependencies examples:

```yaml
dependencies:
  - repository:
      name: ezored/dependency-sample
      type: github
      version: b:master
```
 

```yaml
dependencies:
  - repository:
      name: "${HOME}/Developer/my-local-dependency"
      type: local
``` 

### Documentation Index

- [Back to index](GET-STARTED.md)
