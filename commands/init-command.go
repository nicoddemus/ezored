package commands

import (
	"github.com/ezored/ezored/constants"
	"github.com/ezored/ezored/logger"
	"github.com/ezored/ezored/utils/file-utils"
)

type InitCommand struct {
}

func (This *InitCommand) Init() {
	// project file
	logger.D("Creating project files...")

	if fileutils.Exists(constants.PROJECT_FILENAME) {
		logger.D("Project files already exists")
	} else {
		createProjectFiles()
	}

	// source things
	if fileutils.Exists(constants.SOURCE_DIRECTORY) {
		logger.D("Source files already exists")
	} else {
		createSourceFiles()
	}
}

func createProjectFiles() {
	fileutils.CreateFileWithContent("", constants.PROJECT_FILENAME, fileutils.GetAssetContent("bindata/init-command/ezored-project.json"))
	logger.D("Project file created")
}

func createSourceFiles() {
	// gitkeep
	fileutils.CreateFileWithContent(constants.SOURCE_DIRECTORY, constants.GIT_KEEP_FILENAME, []byte{})
	logger.D("Source files created")
}
