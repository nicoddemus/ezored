package models

import "errors"

type Vendor struct {
	Dependency struct {
		Build []string `json:"build"`
	} `json:"dependency"`
	Targets []*VendorTarget `json:"targets"`
}

type VendorTarget struct {
	Name string                 `json:"name"`
	Data *VendorTargetBuildData `json:"data"`
}

type VendorTargetBuildData struct {
	HeaderSearchPaths    []string    `json:"headerSearchPaths"`
	LibrarySearchPaths   []string    `json:"librarySearchPaths"`
	SourceFiles          []string    `json:"sourceFiles"`
	HeaderFiles          []string    `json:"headerFiles"`
	LibraryLinks         []string    `json:"libraryLinks"`
	FrameworkLinks       []string    `json:"frameworkLinks"`
	CFlags               []string    `json:"cFlags"`
	CXXFlags             []string    `json:"cxxFlags"`
	TargetCompileOptions []string    `json:"targetCompileOptions"`
	CopyFiles            []*CopyFile `json:"copyFiles"`
}

func (This *Vendor) GetTargetByName(name string) (*VendorTarget, error) {
	if This.Targets == nil {
		return nil, errors.New("no targets on this dependency")
	}

	for _, target := range This.Targets {
		if target.Name == name {
			return target, nil
		}
	}

	return nil, errors.New("target not found")
}
