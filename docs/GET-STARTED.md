# Get started

We have created a lot of docs and prebuilt binaries to accelerate development process.  

### Commands

Use the follow pattern to execute commands:  
> ezored \<command\> \<task\>  

More commands:  

- `help`: Show all available commands.
- `init`: Initialize a new project with sample dependencies and required files.
- `dependencies update`: Update all dependencies inside project file.
- `build <target name>`: Build the specified target. If target name is ommited, all targets will be builded.

### Prebuilt

Inside Ezored repository have a folder here called `"build"` with prebuilt binaries for all platforms (windows, mac, linux).

### Get started NOW, please!

Execute the following commands to create a initial directory with all required files:

> mkdir ezored-test  
> cd ezored-test  
> ezored init  
> ezored dependencies update  
> ezored build ios  
> ezored build android  

Obs: 
1. Add `"ezored"` binary to your PATH or use full-path on command line.
2. You can use `"ezored build"` command to build all targets

### Compile from source

> go get -u github.com/ezored/ezored  
> go install github.com/ezored/ezored    