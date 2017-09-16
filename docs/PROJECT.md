# Project

A Ezored project file contains one or more targets inside, that can be build using the Ezored from command-line.
 
The final target project generally is a library that have all native code compiled for target platform.

To build each target inside Ezored project file, we use a bunch of rules included target project and all your dependencies rules.

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