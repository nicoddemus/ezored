# EzoRed

[![Build Status](https://travis-ci.org/ezored/ezored.svg?branch=master)](https://travis-ci.org/ezored/ezored)
[![Coverage Status](https://coveralls.io/repos/github/ezored/ezored/badge.svg?branch=master)](https://coveralls.io/github/ezored/ezored?branchmaster)
<!--[![Github All Releases](https://img.shields.io/github/downloads/ezored/ezored/total.svg)]()-->


<img src="extras/images/doc-logo.png?v=2017-12-07" alt="EzoRed">  

The main goal of this tool is let you make a single C++ code and generate a library for multiple platforms based on targets.    

EzoRed uses a target list inside it project file to the build process. Each target can be an official supported target or your custom target (public, private or local).  

And finally, each target can be modified by project dependencies. One simple example is the HTTP dependency, you dont need write a HTTP Client for iOS or Android, you can use the official HTTP Client dependency.   

Today we have implemented officially this targets:  

- [ios](https://github.com/ezored/target-ios)
- [android](https://github.com/ezored/target-android)

On each target link you can download the demo application from platform store.

All official dependencies and targets are in EzoRed [repository](https://github.com/ezored) page.

## Install

```
pip install ezored 
```

## Documentation

To check out live docs, visit [docs](docs/GET-STARTED.md) folder.

## Changelog

Detailed changes for each release are documented in the [release notes](docs/RELEASE-NOTES.md).

## Contact

You can send email to me, to talk about anything related to the project:  
[paulo@prsolucoes.com](paulo@prsolucoes.com)

## Supported By Jetbrains IntelliJ IDEA

![Supported By Jetbrains IntelliJ IDEA](extras/images/jetbrains-logo.png "Supported By Jetbrains IntelliJ IDEA")

## Author WebSite

> http://www.pcoutinho.com

## License

[MIT](http://opensource.org/licenses/MIT)

Copyright (c) 2017-present, Paulo Coutinho