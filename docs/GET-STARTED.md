# Get started

There is a lot of docs and ready tools to accelerate development process.  

### Installing

Install EzoRed typing in your terminal:

```
pip install ezored 
```

### Commands

Use the follow pattern to execute commands:  
> ezored \<command\> \<task\> \<other-params-if-have\>    

More commands:  

- `-h` or `--help`: Show all available commands.
- `init`: Initialize a new project with sample dependencies and required files.
- `dependency update`: Update all dependencies inside project file.
- `target build <target-name>`: Build the specified target. If target name is ommited, all targets will be builded.
- `clean`: Clean all temporary data

### Get started NOW, please!

Execute the following commands to create a initial directory with all required files:

> mkdir ezored-test  
> cd ezored-test  
> ezored init  
> ezored dependency update  
> ezored target build ios  
> ezored target build android  

Obs: 
1. You can use only `"ezored build"` command to build all targets

### Documentation Index

- [Workflows](WORKFLOWS.md)
- [Project](PROJECT.md)
- [Dependencies](DEPENDENCY.md)
- [Targets](TARGET.md)
- [Release notes](RELEASE-NOTES.md)

