# ezored

[![Build Status](https://travis-ci.org/ezored/ezored.svg?branch=master)](https://travis-ci.org/ezored/ezored)
[![Coverage Status](https://coveralls.io/repos/github/ezored/ezored/badge.svg?branch=master)](https://coveralls.io/github/ezored/ezored?branchmaster)
<!--[![Github All Releases](https://img.shields.io/github/downloads/ezored/ezored/total.svg)]()-->


<img src="extras/images/doc-logo.png?v=2017-12-07" alt="ezored">  

The ezored is a build tool with focus on progressive integration with native code.  

Progressive integration means that if you are building a new application or already have one (mobile, desktop or cli), you can integrate it with a compiled code with ezored.    

Running native code means fast execution (the code is compiled to machine code) and safe execution (since it is harder to disassemble and/or modify).         

Some concepts are used internally to make it happen:
- Dependency: Is a fragment of C++ code. Can be a full http client implementation or can be your private business logic.    
- Target: Is the way of all dependencies are compiled. Each platform has their rules, and the target know it and compile the code using the correct way.  

Today we have implemented officially this targets:  

- [ios](https://github.com/ezored/target-ios)
- [android](https://github.com/ezored/target-android)
- [linux](https://github.com/ezored/target-linux)
- [windows](https://github.com/ezored/target-windows)
- [macos](https://github.com/ezored/target-macos)

All official dependencies and targets are in ezored [repository](https://github.com/ezored) page.

Remember that targets and dependencies can be any git repository, remote zip file or local folders.    

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