# Dependencies

A dependency consists in a small part of software, like a HTTP library, ZIP library, openssl, curl or your custom business code, that will be reused by your other projects.  

### Dependency block structure

The dependency block structure has this properties:  
- type
- name
- version

The property `"type"` define how Ezored will get your dependency. Today we support types:
- local  
- github  

The property `"name"` define how Ezored will find your dependency based on `"type"`. Example:  
- `local` = You need set the path to the dependency directory, ex: `${HOME}/my-dependency`  
- `github` = You need set the repository name, ex: `ezored/dependency-sample` 

The property `"version"` define what version Ezored need download, ex: `"1.2.0"`. Git repositories have some especial version parse rules:
- `b:master` = will download version from branch "master" 
- `t:1.2.0` = will download version from tag "1.2.0" 
- `c:ef016c0` = will download version from commit "ef016c0" 
- `1.2.0` = without prefix will download version from tag "1.2.0" 
- `empty` = empty version field will download version from branch master 

### Example

Some dependencies examples:

```json
{
    "name": "ezored/dependency-djinni-support",
    "type": "github",
    "version": "b:master"
}
```

```json
{
    "name": "ezored/dependency-sample",
    "type": "github",
    "version": "b:master"
}
``` 

```json
{
    "type": "local",
    "name": "${HOME}${EZORED_DS}Developer${EZORED_DS}my-local-dependency"
}
``` 

### Documentation Index

- [Back to index](GET-STARTED.md)
