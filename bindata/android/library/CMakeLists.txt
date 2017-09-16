# Standard setup
cmake_minimum_required(VERSION 3.6)

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

# Flags
set(CMAKE_C_FLAGS "${EZO_CMAKE_C_FLAGS}")
set(CMAKE_CXX_FLAGS "${EZO_CMAKE_CXX_FLAGS}")

target_compile_options({{.ProjectName}} PUBLIC "${EZO_TARGET_COMPILE_OPTIONS}")