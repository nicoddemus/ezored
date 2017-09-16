# Get started

We have created a lot of docs and prebuilt binaries to accelerate development process.  

### Commands

Use the follow pattern to execute commands:  
> ezored \<command\> \<task\>  

More commands:  

- `help`: show all available commands.
- `init`: initialize a new project with sample dependencies and required files.
- `dependencies update`: update all dependencies inside project file.
- `build <build name>`: build library for iOS, Android or any other custom build in your project file.

### Prebuilt

Inside Ezored repository have a folder here called `"build"` with prebuilt binaries for all platforms (windows, mac, linux).

### Get started NOW, please!

Execute the following commands to create a initial directory with all required files:

> mkdir ezored-test  
> cd ezored-test  
> ezored init  
> ezored dependencies update  
> ezored compile ios  
> ezored compile android  

Obs: Add `"ezored"` binary to your PATH or use full-path on command line.

### Compile from source

> go get -u github.com/ezored/ezored  
> go install github.com/ezored/ezored    