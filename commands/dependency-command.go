package commands

import (
	"encoding/json"
	"flag"
	"fmt"
	"github.com/ezored/ezored/constants"
	"github.com/ezored/ezored/logger"
	"github.com/ezored/ezored/models"
	"github.com/ezored/ezored/utils/file-utils"
	"github.com/ezored/ezored/utils/flag-utils"
	"io/ioutil"
	"os"
	"os/exec"
	"path/filepath"
)

const (
	TASK_DEPENDENCIES_UPDATE = "update"
)

type DependenciesCommand struct {
	BaseCommand
}

func (This *DependenciesCommand) Init() {
	if flagutils.CheckForArgsCount(2) {
		task := flag.Arg(1)

		switch task {
		case TASK_DEPENDENCIES_UPDATE:
			This.Update()
		}
	} else {
		logger.F("Invalid dependency task")
	}
}

func (This *DependenciesCommand) Update() {
	project := fileutils.GetProject()

	if !project.HasDependencies() {
		logger.I("Your project has no dependencies")
		return
	}

	logger.D("Updating dependencies...")

	for _, dependency := range project.Dependencies {
		if dependency.Type == models.REPOSITORY_TYPE_GITHUB {
			// prepare
			logger.D("Getting dependency: %s...", dependency.GetName())

			fileutils.CreateDependenciesDirectory()
			fileutils.CreateTemporaryDirectory()

			downloadUrl := dependency.GetDownloadUrl()
			downloadDest := filepath.Join(constants.TEMPORARY_DIRECTORY, dependency.GetFileName())
			workingDirectory := filepath.Join(constants.TEMPORARY_DIRECTORY, dependency.GetDirectoryName())

			// download dependency
			if fileutils.Exists(downloadDest) {
				logger.D("Dependency already downloaded: %s", dependency.GetName())
			} else {
				err := fileutils.DownloadFile(downloadDest, downloadUrl)

				if err != nil {
					logger.F("Problems when download dependency: %s - %s", dependency.GetName(), err)
				}

				if fileutils.Exists(downloadDest) {
					logger.D("Dependency downloaded: %s", dependency.GetName())
				} else {
					logger.F("Problems when obtain dependency: %s", dependency.GetName())
				}
			}

			// extract dependency
			logger.D("Extracting dependency: %s...", dependency.GetName())

			if fileutils.Exists(workingDirectory) {
				logger.D("Dependency already extracted: %s", dependency.GetName())
			} else {
				err := fileutils.Unzip(downloadDest, constants.TEMPORARY_DIRECTORY)

				if err != nil {
					logger.F("Problems when extract dependency: %s - %s", dependency.GetName(), err)
				}

				if fileutils.Exists(workingDirectory) {
					logger.D("Dependency extracted: %s", dependency.GetName())
				} else {
					logger.F("Problems when unzip dependency: %s - %s", dependency.GetName(), err)
				}
			}

			// build dependency
			logger.D("Building dependency: %s...", dependency.GetName())

			// process dependency build command
			fileContent, err := ioutil.ReadFile(filepath.Join(workingDirectory, constants.VENDOR_DEPENDENCY_FILENAME))

			if err != nil {
				logger.F(err.Error())
			}

			var vendorDependency models.Vendor
			err = json.Unmarshal(fileContent, &vendorDependency)

			if err != nil {
				logger.F(err.Error())
			}

			buildCommandParts := vendorDependency.Dependency.Build
			head := buildCommandParts[0]
			buildCommandParts = buildCommandParts[1:]

			cmd := exec.Command(head, buildCommandParts...)
			cmd.Dir = workingDirectory

			// pass environment variables
			currentDir, err := os.Getwd()

			if err != nil {
				logger.F("Problems when build dependency: %s - %s", dependency.GetName(), err)
			}

			env := os.Environ()
			env = append(env, fmt.Sprintf("EZORED_PROJECT_ROOT=%s", currentDir))
			cmd.Env = env

			// execute
			out, err := cmd.Output()

			if err != nil {
				logger.F("Problems when build dependency: %s - %s", dependency.GetName(), err)
			}

			if len(out) > 0 {
				logger.D("Dependency build log:\n\n%s\n", out)
			}

			// remove downloaded file
			os.RemoveAll(downloadDest)

			logger.D("Dependency built: %s", dependency.GetName())
		}
	}

	logger.D("Dependencies updated")
}
