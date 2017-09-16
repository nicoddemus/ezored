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
	"path/filepath"
)

const (
	TASK_BUILD = "build"
)

type BuildCommand struct {
	BaseCommand
}

func (This *BuildCommand) Init() {
	if flagutils.CheckForArgsCount(2) {
		task := flag.Arg(1)

		switch task {
		case TASK_BUILD:
			This.Build()
			break
		}
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
	if len(flag.Args()) > 2 {
		targetName = flag.Arg(2)

		if len(targetName) > 0 {
			buildAllTargets = false
		}
	}

	if buildAllTargets {
		logger.D("Build started for all targets")
	} else {
		logger.D(fmt.Sprintf("Build started for target: %s", targetName))
	}

	targetBuilt := 0

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

		// TODO: Need make the new build process here
		// download target if it is not downloaded

		logger.D("Finished build target: %s", target.Name)

		targetBuilt = targetBuilt + 1
	}

	// prepare directories

	/*
		os.RemoveAll(filepath.Join(constants.BUILD_DIRECTORY, constants.IOS_DIRECTORY))
		fileutils.CreateBuildDirectory()

		workingDirectory := filepath.Join(constants.BUILD_DIRECTORY, constants.IOS_DIRECTORY, constants.BUILD_DIRECTORY)

		// prepare template
		buildFileContent := fileutils.GetAssetContent("bindata/ios/CMakeLists.txt")

		t := template.New("ios")
		t, err = t.Parse(string(buildFileContent))

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

		var buildFileContentBuffer bytes.Buffer
		t.Execute(&buildFileContentBuffer, data)

		// create files
		fileutils.CreateFileWithContent(filepath.Join(constants.BUILD_DIRECTORY, constants.IOS_DIRECTORY), constants.CMAKE_FILE, buildFileContentBuffer.Bytes())
		fileutils.CreateFileWithContent(filepath.Join(constants.BUILD_DIRECTORY, constants.IOS_DIRECTORY, constants.FILES_DIRECTORY), "ios.cmake", fileutils.GetAssetContent("bindata/ios/files/ios.cmake"))

		// copy files
		fileutils.CopyAllFiles(targetCopyFiles)

		// generate files
		os.MkdirAll(workingDirectory, constants.DIRECTORY_PERMISSIONS)

		buildCommand := []string{"cmake", "-DCMAKE_TOOLCHAIN_FILE=../files/ios.cmake", "-DIOS_PLATFORM=OS", "-GXcode", "../"}
		output, err := osutils.Exec(buildCommand, workingDirectory)

		if err != nil {
			logger.F("Problems when generate files for iOS: %s", err)
		}

		if len(output) > 0 {
			logger.D("Generate files for iOS log:\n\n%s\n", output)
		}
	*/

	logger.D("Build for iOS finished")
}

/*
func (This *BuildCommand) buildForIOS() {
	logger.D("Build for iOS started")

	// initial build file content
	headerSearchPaths := []string{}
	librarySearchPaths := []string{}
	sourceFiles := []string{}
	headerFiles := []string{}
	libraryLinks := []string{}
	frameworkLinks := []string{}
	cFlags := []string{}
	cxxFlags := []string{}
	targetCompileOptions := []string{}
	copyFiles := []models.CopyFile{}

	// analyze project dependencies
	fileContent, err := ioutil.ReadFile(constants.PROJECT_FILENAME)

	if err != nil {
		logger.F(err.Error())
	}

	var dependencies []*models.Repository
	err = json.Unmarshal(fileContent, &dependencies)

	if err != nil {
		logger.F(err.Error())
	}

	for _, dependency := range dependencies {
		logger.D("Analyzing dependency: %s...", dependency.Name)

		// get vendor file
		workingDirectory := fmt.Sprintf("%s/%s", constants.TEMPORARY_DIRECTORY, dependency.GetDirectoryName())
		fileContent, err := ioutil.ReadFile(fmt.Sprintf("%s/%s", workingDirectory, constants.VENDOR_DEPENDENCY_FILENAME))

		if err != nil {
			logger.F(err.Error())
		}

		var vendorDependency models.Vendor
		err = json.Unmarshal(fileContent, &vendorDependency)

		if err != nil {
			logger.F(err.Error())
		}

		headerSearchPaths = append(headerSearchPaths, vendorDependency.Build.IOS.HeaderSearchPaths...)
		librarySearchPaths = append(librarySearchPaths, vendorDependency.Build.IOS.LibrarySearchPaths...)
		sourceFiles = append(sourceFiles, vendorDependency.Build.IOS.SourceFiles...)
		headerFiles = append(headerFiles, vendorDependency.Build.IOS.HeaderFiles...)
		libraryLinks = append(libraryLinks, vendorDependency.Build.IOS.LibraryLinks...)
		frameworkLinks = append(frameworkLinks, vendorDependency.Build.IOS.FrameworkLinks...)
		cFlags = append(cFlags, vendorDependency.Build.IOS.CFlags...)
		cxxFlags = append(cxxFlags, vendorDependency.Build.IOS.CXXFlags...)
		targetCompileOptions = append(targetCompileOptions, vendorDependency.Build.IOS.TargetCompileOptions...)
		copyFiles = append(copyFiles, vendorDependency.Build.Android.CopyFiles...)

		logger.D("Analyzed dependency: %s", dependency.Name)
	}

	// prepare directories
	os.RemoveAll(filepath.Join(constants.BUILD_DIRECTORY, constants.IOS_DIRECTORY))
	fileutils.CreateBuildDirectory()

	workingDirectory := filepath.Join(constants.BUILD_DIRECTORY, constants.IOS_DIRECTORY, constants.BUILD_DIRECTORY)

	// prepare template
	buildFileContent := fileutils.GetAssetContent("bindata/ios/CMakeLists.txt")

	t := template.New("ios")
	t, err = t.Parse(string(buildFileContent))

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
		HeaderSearchPaths:    headerSearchPaths,
		LibrarySearchPaths:   librarySearchPaths,
		SourceFiles:          sourceFiles,
		HeaderFiles:          headerFiles,
		LibraryLinks:         libraryLinks,
		FrameworkLinks:       frameworkLinks,
		CFlags:               cFlags,
		CXXFlags:             cxxFlags,
		TargetCompileOptions: targetCompileOptions,
		ProjectName:          constants.DEFAULT_PROJECT_NAME,
	}

	var buildFileContentBuffer bytes.Buffer
	t.Execute(&buildFileContentBuffer, data)

	// create files
	fileutils.CreateFileWithContent(filepath.Join(constants.BUILD_DIRECTORY, constants.IOS_DIRECTORY), constants.CMAKE_FILE, buildFileContentBuffer.Bytes())
	fileutils.CreateFileWithContent(filepath.Join(constants.BUILD_DIRECTORY, constants.IOS_DIRECTORY, constants.FILES_DIRECTORY), "ios.cmake", fileutils.GetAssetContent("bindata/ios/files/ios.cmake"))

	// copy files
	fileutils.CopyAllFiles(copyFiles)

	// generate files
	os.MkdirAll(workingDirectory, constants.DIRECTORY_PERMISSIONS)

	buildCommand := []string{"cmake", "-DCMAKE_TOOLCHAIN_FILE=../files/ios.cmake", "-DIOS_PLATFORM=OS", "-GXcode", "../"}
	output, err := osutils.Exec(buildCommand, workingDirectory)

	if err != nil {
		logger.F("Problems when generate files for iOS: %s", err)
	}

	if len(output) > 0 {
		logger.D("Generate files for iOS log:\n\n%s\n", output)
	}

	logger.D("Build for iOS finished")
}

func (This *BuildCommand) buildForAndroid() {
	logger.D("Build for Android started")

	// initial build file content
	headerSearchPaths := []string{}
	librarySearchPaths := []string{}
	sourceFiles := []string{}
	headerFiles := []string{}
	libraryLinks := []string{}
	frameworkLinks := []string{}
	cFlags := []string{}
	cxxFlags := []string{}
	targetCompileOptions := []string{}
	copyFiles := []models.CopyFile{}

	// analyze project dependencies
	fileContent, err := ioutil.ReadFile(constants.PROJECT_FILENAME)

	if err != nil {
		logger.F(err.Error())
	}

	var dependencies []*models.Repository
	err = json.Unmarshal(fileContent, &dependencies)

	if err != nil {
		logger.F(err.Error())
	}

	for _, dependency := range dependencies {
		logger.D("Analyzing dependency: %s...", dependency.Name)

		// get vendor file
		workingDirectory := fmt.Sprintf("%s/%s", constants.TEMPORARY_DIRECTORY, dependency.GetDirectoryName())
		fileContent, err := ioutil.ReadFile(fmt.Sprintf("%s/%s", workingDirectory, constants.VENDOR_DEPENDENCY_FILENAME))

		if err != nil {
			logger.F(err.Error())
		}

		var vendorDependency models.Vendor
		err = json.Unmarshal(fileContent, &vendorDependency)

		if err != nil {
			logger.F(err.Error())
		}

		headerSearchPaths = append(headerSearchPaths, vendorDependency.Build.Android.HeaderSearchPaths...)
		librarySearchPaths = append(librarySearchPaths, vendorDependency.Build.Android.LibrarySearchPaths...)
		sourceFiles = append(sourceFiles, vendorDependency.Build.Android.SourceFiles...)
		headerFiles = append(headerFiles, vendorDependency.Build.Android.HeaderFiles...)
		libraryLinks = append(libraryLinks, vendorDependency.Build.Android.LibraryLinks...)
		frameworkLinks = append(frameworkLinks, vendorDependency.Build.Android.FrameworkLinks...)
		cFlags = append(cFlags, vendorDependency.Build.Android.CFlags...)
		cxxFlags = append(cxxFlags, vendorDependency.Build.Android.CXXFlags...)
		targetCompileOptions = append(targetCompileOptions, vendorDependency.Build.Android.TargetCompileOptions...)
		copyFiles = append(copyFiles, vendorDependency.Build.Android.CopyFiles...)

		logger.D("Analyzed dependency: %s", dependency.Name)
	}

	// prepare directories
	os.RemoveAll(filepath.Join(constants.BUILD_DIRECTORY, constants.ANDROID_DIRECTORY))
	fileutils.CreateBuildDirectory()

	workingDirectory := filepath.Join(constants.BUILD_DIRECTORY, constants.ANDROID_DIRECTORY)

	// prepare template
	buildFileContent := fileutils.GetAssetContent("bindata/android/library/CMakeLists.txt")

	t := template.New("android")
	t, err = t.Parse(string(buildFileContent))

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
		HeaderSearchPaths:    headerSearchPaths,
		LibrarySearchPaths:   librarySearchPaths,
		SourceFiles:          sourceFiles,
		HeaderFiles:          headerFiles,
		LibraryLinks:         libraryLinks,
		FrameworkLinks:       frameworkLinks,
		CFlags:               cFlags,
		CXXFlags:             cxxFlags,
		TargetCompileOptions: targetCompileOptions,
		ProjectName:          constants.DEFAULT_PROJECT_NAME,
	}

	var buildFileContentBuffer bytes.Buffer
	t.Execute(&buildFileContentBuffer, data)

	// create files
	fileutils.CreateFileWithContent(filepath.Join(constants.BUILD_DIRECTORY, constants.ANDROID_DIRECTORY, "library"), constants.CMAKE_FILE, buildFileContentBuffer.Bytes())
	fileutils.CreateFileWithContent(filepath.Join(constants.BUILD_DIRECTORY, constants.ANDROID_DIRECTORY, "library"), "build.gradle", fileutils.GetAssetContent("bindata/android/library/build.gradle"))
	fileutils.CreateFileWithContent(filepath.Join(constants.BUILD_DIRECTORY, constants.ANDROID_DIRECTORY, "library", "src", "main"), "AndroidManifest.xml", fileutils.GetAssetContent("bindata/android/library/src/main/AndroidManifest.xml"))
	fileutils.CreateFileWithContent(filepath.Join(constants.BUILD_DIRECTORY, constants.ANDROID_DIRECTORY, "gradle", "wrapper"), "gradle-wrapper.jar", fileutils.GetAssetContent("bindata/android/gradle/wrapper/gradle-wrapper.jar"))
	fileutils.CreateFileWithContent(filepath.Join(constants.BUILD_DIRECTORY, constants.ANDROID_DIRECTORY, "gradle", "wrapper"), "gradle-wrapper.properties", fileutils.GetAssetContent("bindata/android/gradle/wrapper/gradle-wrapper.properties"))
	fileutils.CreateFileWithContent(filepath.Join(constants.BUILD_DIRECTORY, constants.ANDROID_DIRECTORY), "build.gradle", fileutils.GetAssetContent("bindata/android/build.gradle"))
	fileutils.CreateFileWithContent(filepath.Join(constants.BUILD_DIRECTORY, constants.ANDROID_DIRECTORY), "gradle.properties", fileutils.GetAssetContent("bindata/android/gradle.properties"))
	fileutils.CreateFileWithContent(filepath.Join(constants.BUILD_DIRECTORY, constants.ANDROID_DIRECTORY), "gradlew", fileutils.GetAssetContent("bindata/android/gradlew"))
	fileutils.CreateFileWithContent(filepath.Join(constants.BUILD_DIRECTORY, constants.ANDROID_DIRECTORY), "gradlew.bat", fileutils.GetAssetContent("bindata/android/gradlew.bat"))
	fileutils.CreateFileWithContent(filepath.Join(constants.BUILD_DIRECTORY, constants.ANDROID_DIRECTORY), "settings.gradle", fileutils.GetAssetContent("bindata/android/settings.gradle"))

	// make files executables
	os.Chmod(filepath.Join(constants.BUILD_DIRECTORY, constants.ANDROID_DIRECTORY, "gradlew"), constants.EXECUTABLE_FILE_PERMISSIONS)

	// copy files
	fileutils.CopyAllFiles(copyFiles)

	// generate files
	prefixCommand := "./"

	if osutils.IsWindows() {
		prefixCommand = ""
	}

	buildCommand := []string{prefixCommand + "gradlew", "build", "--debug", "--stacktrace"}

	output, err := osutils.Exec(buildCommand, workingDirectory)

	if err != nil {
		logger.F("Problems when generate files for Android: %s", err)
	}

	if len(output) > 0 {
		logger.D("Generate files for Android log:\n\n%s\n", output)
	}

	logger.D("Build for Android finished")
}
*/
