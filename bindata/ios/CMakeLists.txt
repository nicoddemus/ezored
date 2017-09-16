# Standard setup
cmake_minimum_required(VERSION 3.9)

set(DEVELOPMENT_PROJECT_NAME "{{.ProjectName}}") # <== Set to your project name, e.g. project.xcodeproj
set(DEVELOPMENT_TEAM_ID "99AHAA343Q") # <== Set to your team ID from Apple
set(FRAMEWORK_NAME "Ezo") # <== Set to your framework's name
set(FRAMEWORK_BUNDLE_IDENTIFIER "com.ezored.test") # <== Set to your framework's bundle ID
set(CODE_SIGN_IDENTITY "iPhone Developer") # <== Set to your preferred code sign identity, to see list: /usr/bin/env xcrun security find-identity -v -p codesigning
set(DEPLOYMENT_TARGET 8.0) # <== Set your deployment target version of iOS
set(DEVICE_FAMILY "1,2") # <== Set to "1" to target iPhone, set to "2" to target iPad, set to "1,2" to target both

set(VERSION "1.0.0")
set(SOVERSION "1.0.0")

project({{.ProjectName}})

# Header search paths
set(EZO_HEADER_SEARCH_PATHS
{{range .HeaderSearchPaths}}
    "{{.}}"
{{end}}
)

include_directories(${EZO_HEADER_SEARCH_PATHS})

# Library search paths
set(EZO_LIBRARY_SEARCH_PATHS
{{range .LibrarySearchPaths}}
    "{{.}}"
{{end}}
)

link_directories(${EZO_LIBRARY_SEARCH_PATHS})

# Source files
set(EZO_SOURCE_FILES
{{range .SourceFiles}}
	"{{.}}"
{{end}}
{{range .HeaderFiles}}
	"{{.}}"
{{end}}
)

# Header files
set(EZO_HEADER_FILES
{{range .HeaderFiles}}
	"{{.}}"
{{end}}
)

# Framework links
set(EZO_FRAMEWORK_LINKS
"{{range .FrameworkLinks}} -framework {{.}} {{end}}"
)

string(STRIP "${EZO_FRAMEWORK_LINKS}" EZO_FRAMEWORK_LINKS)

# Library links
set(EZO_LIBRARY_LINKS
"{{range .LibraryLinks}} {{.}} {{end}}"
)

string(STRIP "${EZO_LIBRARY_LINKS}" EZO_LIBRARY_LINKS)

# CFlags
set(EZO_CMAKE_C_FLAGS
"{{range .CFlags}} {{.}} {{end}}"
)

string(STRIP "${EZO_CMAKE_C_FLAGS}" EZO_CMAKE_C_FLAGS)

# CXXFlags
set(EZO_CMAKE_CXX_FLAGS
"{{range .CXXFlags}} {{.}} {{end}}"
)

string(STRIP "${EZO_CMAKE_CXX_FLAGS}" EZO_CMAKE_CXX_FLAGS)

# Target compile options
set(EZO_TARGET_COMPILE_OPTIONS
"{{range .TargetCompileOptions}} {{.}} {{end}}"
)

string(STRIP "${EZO_TARGET_COMPILE_OPTIONS}" EZO_TARGET_COMPILE_OPTIONS)

# Library
add_library({{.ProjectName}} SHARED ${EZO_SOURCE_FILES})

# Target links
target_link_libraries({{.ProjectName}} "${EZO_LIBRARY_LINKS}")
target_link_libraries({{.ProjectName}} "${EZO_FRAMEWORK_LINKS}")

# Flags
set(CMAKE_C_FLAGS "${EZO_CMAKE_C_FLAGS}")
set(CMAKE_CXX_FLAGS "${EZO_CMAKE_CXX_FLAGS}")

set_target_properties({{.ProjectName}} PROPERTIES
    CXX_STANDARD 11
    CXX_STANDARD_REQUIRED true
    CXX_EXTENSIONS false
    FRAMEWORK TRUE
    FRAMEWORK_VERSION A
    MACOSX_FRAMEWORK_IDENTIFIER ${FRAMEWORK_BUNDLE_IDENTIFIER}
    MACOSX_FRAMEWORK_BUNDLE_VERSION "${VERSION}"
    VERSION "${VERSION}"
    SOVERSION "${SOVERSION}"
    PUBLIC_HEADER "${EZO_HEADER_FILES}"
    XCODE_ATTRIBUTE_IPHONEOS_DEPLOYMENT_TARGET ${DEPLOYMENT_TARGET}
    XCODE_ATTRIBUTE_CODE_SIGN_IDENTITY ${CODE_SIGN_IDENTITY}
    XCODE_ATTRIBUTE_DEVELOPMENT_TEAM ${DEVELOPMENT_TEAM_ID}
    XCODE_ATTRIBUTE_TARGETED_DEVICE_FAMILY ${DEVICE_FAMILY}
    XCODE_ATTRIBUTE_ONLY_ACTIVE_ARCH NO
    XCODE_ATTRIBUTE_SKIP_INSTALL YES
    GCC_GENERATE_DEBUGGING_SYMBOLS YES
    XCODE_ATTRIBUTE_INSTALL_PATH "@loader_path/Frameworks"
)

target_compile_options({{.ProjectName}} PUBLIC "${EZO_TARGET_COMPILE_OPTIONS}")