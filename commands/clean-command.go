package commands

import (
	"github.com/ezored/ezored/constants"
	"github.com/prsolucoes/pickman/logger"
	"os"
)

type CleanCommand struct {
}

func (This *CleanCommand) Init() {
	logger.D("Cleaning...")
	os.RemoveAll(constants.TEMPORARY_DIRECTORY)
	os.RemoveAll(constants.BUILD_DIRECTORY)
	os.RemoveAll(constants.TARGET_DIRECTORY)
	os.RemoveAll(constants.VENDOR_DIRECTORY)
	logger.D("Finished")
}
