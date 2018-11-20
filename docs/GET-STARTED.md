# Get started

There is a lot of docs and ready tools to accelerate development process.  

### Installing

Install ezored typing in your terminal:

```
pip install ezored 
```

or, if you have permission problem, use:

```
pip install ezored --user 
```

### Commands

Use the follow pattern to execute commands:  
> ezored \<command\> \<task\> \<other-params-if-have\>    

More commands:  

- `-h` or `--help`: Show all available commands.
- `init`: Initialize a new project with sample dependencies and required files.
- `dependency install`: Install all dependencies inside project file.
- `dependency install <dependency-name>`: Install a single dependency inside project file.
- `target build`: Build all targets inside project file.
- `target build <target-name>`: Build a single target inside project file.
- `clean`: Clean all temporary and downloaded data

### Get started NOW, please!

Execute the following commands to create a initial directory with all required files:

> mkdir ezored-test  
> cd ezored-test  
> ezored init  
> ezored dependency install  
> ezored target build [linux, macos or windows] 


** You can use only `"ezored build <target-name>"` command to build a single target.  
** You can use `"ezored build [ios or android]"` if you have everything installed for it.   

### Documentation Index

- [Workflows](WORKFLOWS.md)
- [Project](PROJECT.md)
- [Dependencies](DEPENDENCY.md)
- [Targets](TARGET.md)
- [Release notes](RELEASE-NOTES.md)

