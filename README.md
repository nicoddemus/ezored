# ezored

[![Build Status](https://travis-ci.org/ezored/ezored.svg?branch=master)](https://travis-ci.org/ezored/ezored)
[![Coverage Status](https://coveralls.io/repos/github/ezored/ezored/badge.svg?branch=master)](https://coveralls.io/github/ezored/ezored?branchmaster)
<!--[![Github All Releases](https://img.shields.io/github/downloads/ezored/ezored/total.svg)]()-->


<img src="extras/images/doc-logo.png?v=2017-12-07" alt="ezored">  

Ezored is a build tool with focus on progressive integration with native code.

Ezored has everything that you need to integrative native C++ code into your current application (mobile, desktop etc), because native code is more secure and faster.     

The main goal of ezored is let you code a single C++ code and generate a library for multiple platforms, instead of write the same business logic code in all used languages and for all used platforms.    

Progressive integration let you attach ezored generated library into your current application or into a new application as part of it. The aim is not replace platform UI code, but the business logic code.

Ezored use a dependency concept to fragment parts of your C++ code into small modules (you business logic classes, log classes, http client classes, helper classes).  

Ezored use a target concept to understand how it will compile the C++ code (joining all dependency C++ code) and generate the final library file (.so, .a, .framework, .dll, dylib etc).     

Today we have implemented officially this targets:  

- [ios](https://github.com/ezored/target-ios)
- [android](https://github.com/ezored/target-android)
- [linux](https://github.com/ezored/target-linux)
- [windows](https://github.com/ezored/target-windows)
- [macos](https://github.com/ezored/target-macos)

All official dependencies and targets are in ezored [repository](https://github.com/ezored) page.

Remember that targets and dependencies can be any repository, local or remote (github).  

## Install

```
pip install ezored 
```

If you have problems with permission, try:

```
pip install ezored --user 
```

## Documentation

To check out live docs, visit [docs](docs/GET-STARTED.md) folder.

## Changelog

Detailed changes for each release are documented in the [release notes](docs/RELEASE-NOTES.md).

## Diagram

<img src="extras/images/what-is.png?v=2018-08-09" alt="ezored - what is" style="max-width: 300px;">

## Supported By Jetbrains IntelliJ IDEA

![Supported By Jetbrains IntelliJ IDEA](extras/images/jetbrains-logo.png "Supported By Jetbrains IntelliJ IDEA")

## License

[MIT](http://opensource.org/licenses/MIT)

Copyright (c) 2017-present, Paulo Coutinho