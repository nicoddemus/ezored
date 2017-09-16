package commands

import "fmt"

type HelpCommand struct {
}

func (This *HelpCommand) Init() {
	fmt.Println("Usage of this tool:")
	fmt.Println("  > help")
	fmt.Println("  > init")
	fmt.Println("  > dependencies")
	fmt.Println("     - update")
	fmt.Println("  > build")
	fmt.Println("     - ios")
	fmt.Println("     - buildForAndroid")
}
