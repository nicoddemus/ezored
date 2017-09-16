package commands

import (
	"bytes"
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
	"text/template"
)

type BuildCommand struct {
	BaseCommand
}

func (This *BuildCommand) Init() {
	if flagutils.CheckForArgsCount(1) {
		This.Build()
	} else {
		logger.F("Invalid build task")
	}
}

func (This *BuildCommand) Build() {
	// setup
	targetName := ""
	buildAllTargets := true
	project := fileutils.GetProject()

	targetHeaderSearchPaths := []string{}
	targetLibrarySearchPaths := []string{}
	targetSourceFiles := []string{}
	targetHeaderFiles := []string{}
	targetLibraryLinks := []string{}
	targetFrameworkLinks := []string{}
	targetCFlags := []string{}
	targetCXXFlags := []string{}
	targetTargetCompileOptions := []string{}
	targetCopyFiles := []*models.CopyFile{}

	// check if project has targets
	if !project.HasTargets() {
		logger.F("Your project has no targets")
	}

	// check if we need build a specifc target or all targets
	fmt.Print(flag.Args())

	if len(flag.Args()) > 1 {
		targetName = flag.Arg(1)

		if len(targetName) > 0 {
			buildAllTargets = false
		}
	}

	if buildAllTargets {
		logger.D("Build started for all targets")
	} else {
		logger.D(fmt.Sprintf("Build started for target: %s", targetName))
	}

	targetsBuilt := 0

	// build targets
	for _, target := range project.Targets {
		if !buildAllTargets {
			if target.Name != targetName {
				continue
			}
		}

		logger.D("Building target: %s...", target.Name)

		// analyze project dependencies
		if project.HasDependencies() {
			for _, dependency := range project.Dependencies {
				logger.D("Analyzing dependency: %s...", dependency.Name)

				// get vendor file
				dependencyWorkingDirectory := filepath.Join(constants.TEMPORARY_DIRECTORY, dependency.GetDirectoryName())
				fileContent, err := ioutil.ReadFile(filepath.Join(dependencyWorkingDirectory, constants.VENDOR_DEPENDENCY_FILENAME))

				if err != nil {
					logger.F(err.Error())
				}

				var vendorDependency models.Vendor
				err = json.Unmarshal(fileContent, &vendorDependency)

				if err != nil {
					logger.F(err.Error())
				}

				// get dependency target data to the current target
				vendorTarget, err := vendorDependency.GetTargetByName(target.Name)

				if err == nil {
					targetHeaderSearchPaths = append(targetHeaderSearchPaths, vendorTarget.Data.HeaderSearchPaths...)
					targetLibrarySearchPaths = append(targetLibrarySearchPaths, vendorTarget.Data.LibrarySearchPaths...)
					targetSourceFiles = append(targetSourceFiles, vendorTarget.Data.SourceFiles...)
					targetHeaderFiles = append(targetHeaderFiles, vendorTarget.Data.HeaderFiles...)
					targetLibraryLinks = append(targetLibraryLinks, vendorTarget.Data.LibraryLinks...)
					targetFrameworkLinks = append(targetFrameworkLinks, vendorTarget.Data.FrameworkLinks...)
					targetCFlags = append(targetCFlags, vendorTarget.Data.CFlags...)
					targetCXXFlags = append(targetCXXFlags, vendorTarget.Data.CXXFlags...)
					targetTargetCompileOptions = append(targetTargetCompileOptions, vendorTarget.Data.TargetCompileOptions...)
					targetCopyFiles = append(targetCopyFiles, vendorTarget.Data.CopyFiles...)
				}

				logger.D("Dependency analyzed: %s", dependency.Name)
			}
		} else {
			logger.I("Your project has no dependencies")
		}

		logger.D("Checking target files...")

		targetTempDirectory := ""

		if target.Repository.Type == models.REPOSITORY_TYPE_GITHUB {
			// prepare
			logger.D("Obtaining target files: %s...", target.Name)

			fileutils.CreateTargetDirectory()
			fileutils.CreateTemporaryDirectory()

			downloadUrl := target.Repository.GetDownloadUrl()
			downloadDest := filepath.Join(constants.TEMPORARY_DIRECTORY, target.Repository.GetFileName())
			workingDirectory := filepath.Join(constants.TEMPORARY_DIRECTORY, target.Repository.GetDirectoryName())
			targetTempDirectory = workingDirectory

			// download target files
			if fileutils.Exists(downloadDest) {
				logger.D("Target files already downloaded: %s", target.Name)
			} else {
				err := fileutils.DownloadFile(downloadDest, downloadUrl)

				if err != nil {
					logger.F("Problems when download target files: %s - %s", target.Name, err)
				}

				if fileutils.Exists(downloadDest) {
					logger.D("Target files downloaded: %s", target.Name)
				} else {
					logger.F("Problems when obtain target files: %s", target.Name)
				}
			}

			// extract target
			logger.D("Extracting target: %s...", target.Name)

			if fileutils.Exists(workingDirectory) {
				logger.D("Target already extracted: %s", target.Name)
			} else {
				err := fileutils.Unzip(downloadDest, constants.TEMPORARY_DIRECTORY)

				if err != nil {
					logger.F("Problems when extract target: %s - %s", target.Name, err)
				}

				if fileutils.Exists(workingDirectory) {
					logger.D("Target extracted: %s", target.Name)
				} else {
					logger.F("Problems when unzip target: %s - %s", target.Name, err)
				}
			}

			// remove downloaded file
			os.RemoveAll(downloadDest)
		}

		// preparing target
		logger.D("Preparing target files...")

		os.RemoveAll(filepath.Join(constants.TARGET_DIRECTORY, target.Name))

		targetProject := fileutils.GetTarget(targetTempDirectory)

		buildCommandParts := targetProject.Target.Build
		head := buildCommandParts[0]
		buildCommandParts = buildCommandParts[1:]

		cmd := exec.Command(head, buildCommandParts...)
		cmd.Dir = targetTempDirectory

		// pass environment variables
		currentDir, err := os.Getwd()

		if err != nil {
			logger.F("Problems when prepare to build target: %s - %s", target.Name, err)
		}

		env := os.Environ()
		env = append(env, fmt.Sprintf("EZORED_PROJECT_ROOT=%s", currentDir))
		cmd.Env = env

		// execute
		out, err := cmd.Output()

		if err != nil {
			logger.F("Problems when prepare to build target: %s - %s", target.Name, err)
		}

		if len(out) > 0 {
			logger.D("Prepare target files to build log:\n\n%s\n", out)
		}

		// copy files to build directory
		os.RemoveAll(filepath.Join(constants.BUILD_DIRECTORY, target.Name))
		fileutils.CopyDir(filepath.Join(constants.TARGET_DIRECTORY, target.Name), filepath.Join(constants.BUILD_DIRECTORY, target.Name))

		// parse files
		if targetProject.Target.ParseFiles != nil && len(targetProject.Target.ParseFiles) > 0 {
			for _, file := range targetProject.Target.ParseFiles {
				templateFilePath := filepath.Join(constants.BUILD_DIRECTORY, target.Name, file)
				fileContent, err := ioutil.ReadFile(templateFilePath)

				if err != nil {
					logger.F(err.Error())
				}

				t := template.New(file)
				t, err = t.Parse(string(fileContent))

				if err != nil {
					logger.F(err.Error())
				}

				data := struct {
					HeaderSearchPaths    []string
					LibrarySearchPaths   []string
					SourceFiles          []string
					HeaderFiles          []string
					LibraryLinks         []string
					FrameworkLinks       []string
					CFlags               []string
					CXXFlags             []string
					TargetCompileOptions []string
					ProjectName          string
				}{
					HeaderSearchPaths:    targetHeaderSearchPaths,
					LibrarySearchPaths:   targetLibrarySearchPaths,
					SourceFiles:          targetSourceFiles,
					HeaderFiles:          targetHeaderFiles,
					LibraryLinks:         targetLibraryLinks,
					FrameworkLinks:       targetFrameworkLinks,
					CFlags:               targetCFlags,
					CXXFlags:             targetCXXFlags,
					TargetCompileOptions: targetTargetCompileOptions,
					ProjectName:          constants.DEFAULT_PROJECT_NAME,
				}

				var fileContentBuffer bytes.Buffer
				t.Execute(&fileContentBuffer, data)

				// replace content
				templateFilePathDir := filepath.Dir(templateFilePath)
				templateFilePathFilename := filepath.Base(templateFilePath)
				fileutils.CreateFileWithContent(templateFilePathDir, templateFilePathFilename, fileContentBuffer.Bytes())
			}
		}

		logger.D("Building target project: %s", target.Name)

		targetBuildDirectory := filepath.Join(constants.BUILD_DIRECTORY, target.Name)
		targetProject = fileutils.GetTarget(targetBuildDirectory)

		buildCommandParts = targetProject.Target.Build
		head = buildCommandParts[0]
		buildCommandParts = buildCommandParts[1:]

		cmd = exec.Command(head, buildCommandParts...)
		cmd.Dir = targetBuildDirectory

		// pass environment variables
		currentDir, err = os.Getwd()

		if err != nil {
			logger.F("Problems when prepare to build target project: %s - %s", target.Name, err)
		}

		env = os.Environ()
		env = append(env, fmt.Sprintf("EZORED_PROJECT_ROOT=%s", currentDir))
		cmd.Env = env

		// execute
		out, err = cmd.Output()

		if err != nil {
			logger.F("Problems when prepare to build target project: %s - %s", target.Name, err)
		}

		if len(out) > 0 {
			logger.D("Target project build log:\n\n%s\n", out)
		}

		logger.D("Finished build target: %s", target.Name)

		targetsBuilt = targetsBuilt + 1
	}

	if targetsBuilt == 0 {
		logger.D("No targets built")
	} else {
		logger.D("Targets built: %d", targetsBuilt)
	}
}
