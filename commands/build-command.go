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
	"github.com/ezored/ezored/utils/os-utils"
	"io/ioutil"
	"os"
	"path/filepath"
	"text/template"
)

type BuildCommand struct {
	BaseCommand
	ProcessData *models.ProcessData
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
	This.ProcessData = &models.ProcessData{}
	This.ProcessData.Reset()

	targetName := ""
	buildAllTargets := true
	project := fileutils.GetProject()
	This.ProcessData.ProjectName = project.GetConfigValueAsString("name")

	// check if project has targets
	if !project.HasTargets() {
		logger.F("Your project has no targets")
	}

	// check if we need build a specific target or all targets
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

		// setup
		logger.D("Building target: %s...", target.Name)

		This.ProcessData.SetTargetName(target.Name)

		targetData := &models.TargetData{}
		targetData.ProjectConfig = project.Config

		// analyze project dependencies
		if project.HasDependencies() {
			for _, dependency := range project.Dependencies {
				dependency.Prepare(This.ProcessData)

				logger.D("Analyzing dependency: %s...", dependency.GetName())

				// get vendor file
				dependencyWorkingDirectory := dependency.GetTempWorkingDir()

				This.ProcessData.DependencyName = dependency.GetName()
				This.ProcessData.RepositoryDir = dependency.GetFullRepositoryDir()

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
					targetData.HeaderSearchPaths = append(targetData.HeaderSearchPaths, vendorTarget.Data.HeaderSearchPaths...)
					targetData.LibrarySearchPaths = append(targetData.LibrarySearchPaths, vendorTarget.Data.LibrarySearchPaths...)
					targetData.SourceFiles = append(targetData.SourceFiles, vendorTarget.Data.SourceFiles...)
					targetData.HeaderFiles = append(targetData.HeaderFiles, vendorTarget.Data.HeaderFiles...)
					targetData.LibraryLinks = append(targetData.LibraryLinks, vendorTarget.Data.LibraryLinks...)
					targetData.FrameworkLinks = append(targetData.FrameworkLinks, vendorTarget.Data.FrameworkLinks...)
					targetData.CFlags = append(targetData.CFlags, vendorTarget.Data.CFlags...)
					targetData.CXXFlags = append(targetData.CXXFlags, vendorTarget.Data.CXXFlags...)
					targetData.CompileOptions = append(targetData.CompileOptions, vendorTarget.Data.TargetCompileOptions...)
					targetData.CopyFiles = append(targetData.CopyFiles, vendorTarget.Data.CopyFiles...)
				}

				targetData.ParseAll(This.ProcessData)

				logger.D("Dependency analyzed: %s", dependency.GetName())
			}

			This.ProcessData.DependencyName = ""
			This.ProcessData.RepositoryDir = ""
		} else {
			logger.I("Your project has no dependencies")
		}

		logger.D("Checking target files...")

		// set data about target repository
		targetTempDirectory := ""
		This.ProcessData.RepositoryDir = target.Repository.GetFullRepositoryDir()
		target.Repository.Prepare(This.ProcessData)

		if target.Repository.Type == models.REPOSITORY_TYPE_GITHUB {
			// prepare
			logger.D("Obtaining target files: %s...", target.Name)

			fileutils.CreateTargetDirectory()
			fileutils.CreateTemporaryDirectory()

			downloadUrl := target.Repository.GetDownloadUrl()
			downloadDest := filepath.Join(constants.TEMPORARY_DIRECTORY, target.Repository.GetFileName())
			workingDirectory := target.Repository.GetTempWorkingDir()
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
		} else if target.Repository.Type == models.REPOSITORY_TYPE_LOCAL {
			// prepare
			logger.D("Obtaining target files: %s...", target.Name)

			fileutils.CreateTargetDirectory()
			fileutils.CreateTemporaryDirectory()

			workingDirectory := target.Repository.GetTempWorkingDir()
			targetTempDirectory = workingDirectory
		}

		// preparing target (basically copy things from temp to target folder)
		logger.D("Preparing target files...")

		os.RemoveAll(filepath.Join(constants.TARGET_DIRECTORY, target.Name))

		targetProject := fileutils.GetTarget(targetTempDirectory)
		output, err := osutils.Exec(targetProject.Target.Build, targetTempDirectory, This.ProcessData.GetEnviron())

		if err != nil {
			logger.F("Problems when prepare to build target: %s - %s", target.Name, err)
		}

		if len(output) > 0 {
			logger.D("Prepare target files to build log:\n\n%s\n", output)
		}

		targetDirectory := filepath.Join(constants.TARGET_DIRECTORY, target.Name)
		targetProject = fileutils.GetTarget(targetDirectory)

		// copy files from dependencies to target directory
		logger.D("Copying files from dependencies...")
		fileutils.CopyAllFiles(targetData.CopyFiles)

		// parse files
		logger.D("Parsing files...")
		targetProject.Target.ParseFiles = This.ProcessData.ParseStringList(targetProject.Target.ParseFiles)

		if targetProject.Target.ParseFiles != nil && len(targetProject.Target.ParseFiles) > 0 {
			for _, file := range targetProject.Target.ParseFiles {
				// parse file
				fileContent, err := ioutil.ReadFile(file)

				if err != nil {
					logger.F(err.Error())
				}

				t := template.New(file)
				t, err = t.Parse(string(fileContent))

				if err != nil {
					logger.F(err.Error())
				}

				var fileContentBuffer bytes.Buffer
				t.Execute(&fileContentBuffer, targetData)

				// replace content
				templateFilePathDir := filepath.Dir(file)
				templateFilePathFilename := filepath.Base(file)
				fileutils.CreateFileWithContent(templateFilePathDir, templateFilePathFilename, fileContentBuffer.Bytes())
			}
		}

		// remove build directory to this target
		logger.D("Removing build directory for this target...")
		os.RemoveAll(filepath.Join(constants.BUILD_DIRECTORY, target.Name))

		// build target (basically the project will be compiled and it need copy correct files to build folder)
		logger.D("Building target project: %s...", target.Name)
		output, err = osutils.Exec(targetProject.Target.Build, targetDirectory, This.ProcessData.GetEnviron())

		if err != nil {
			logger.F("Problems when build target project: %s - %s", target.Name, err)
		}

		if len(output) > 0 {
			logger.D("Target project build log:\n\n%s\n", output)
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
