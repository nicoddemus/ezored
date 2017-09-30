# Project

A Ezored project file contains one or more targets inside, that you can build using the Ezored from command-line.
 
The final target project generally is a library that have all native code compiled for target specific platform.

To build each target inside Ezored project file, we use a bunch of rules, including target project and all project dependencies rules.

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

A sample Ezored project file:

```json
{
	"config": {
		"name": "MyProject"
	},
	"targets": [
		{
			"name": "ios",
			"repository": {
				"name": "ezored/target-ios",
				"type": "github",
				"version": "b:master"
			}
		},
		{
			"name": "android",
			"repository": {
				"name": "ezored/target-android",
				"type": "github",
				"version": "b:master"
			}
		}
	],
	"dependencies": [
		{
			"name": "ezored/dependency-djinni-support",
			"type": "github",
			"version": "b:master"
		},
		{
			"name": "ezored/dependency-sample",
			"type": "github",
			"version": "b:master"
		}
	]
}
```

### Thoubleshoots

- Use only valid chars on config "name" `[a-z][A-Z][0-9]`. Dont start the name with numbers.