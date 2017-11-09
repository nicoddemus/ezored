package commands

import (
	"fmt"
	"github.com/ezored/ezored/utils/file-utils"
)

type HelpCommand struct {
}

func (This *HelpCommand) Init() {
	fmt.Println("Usage of this tool:")
	fmt.Println("  > help")
	fmt.Println("  > init")
	fmt.Println("  > dependencies")
	fmt.Println("     - update")
	fmt.Println("  > build")

	project := fileutils.GetProject()

	if project.HasTargets() {
		for _, target := range project.Targets {
			fmt.Println("     - " + target.Name)
		}	
	} else {
		fmt.Println("     <no targets>")
	}
}
