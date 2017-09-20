package models

type TargetData struct {
	ProjectName        string
	HeaderSearchPaths  []string
	LibrarySearchPaths []string
	SourceFiles        []string
	HeaderFiles        []string
	LibraryLinks       []string
	FrameworkLinks     []string
	CFlags             []string
	CXXFlags           []string
	CompileOptions     []string
	CopyFiles          []*CopyFile
}

func (This *TargetData) ParseAll(data *ProcessData) {
	This.ProjectName = data.ParseString(data.ProjectName)
	This.HeaderSearchPaths = data.ParseStringList(This.HeaderSearchPaths)
	This.LibrarySearchPaths = data.ParseStringList(This.LibrarySearchPaths)
	This.SourceFiles = data.ParseStringList(This.SourceFiles)
	This.HeaderFiles = data.ParseStringList(This.HeaderFiles)
	This.LibraryLinks = data.ParseStringList(This.LibraryLinks)
	This.FrameworkLinks = data.ParseStringList(This.FrameworkLinks)
	This.CFlags = data.ParseStringList(This.CFlags)
	This.CXXFlags = data.ParseStringList(This.CXXFlags)
	This.CompileOptions = data.ParseStringList(This.CompileOptions)
	This.CopyFiles = data.ParseCopyFileList(This.CopyFiles)
}
