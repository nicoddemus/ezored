package models

import (
	"fmt"
	"github.com/ezored/ezored/constants"
	"github.com/ezored/ezored/utils/os-utils"
	"github.com/gosimple/slug"
	"path/filepath"
	"regexp"
	"strings"
)

const (
	REPOSITORY_TYPE_GITHUB = "github"
	REPOSITORY_TYPE_LOCAL  = "local"

	GIT_REPOSITORY_TYPE_TAG    = "t"
	GIT_REPOSITORY_TYPE_BRANCH = "b"
	GIT_REPOSITORY_TYPE_COMMIT = "c"
)

type Repository struct {
	Name    string `json:"name"`
	Type    string `json:"type"`
	Version string `json:"version"`
}

func (This *Repository) GetName() string {
	if This.Type == REPOSITORY_TYPE_LOCAL {
		_, file := filepath.Split(This.Name)
		return file
	}

	return This.Name
}

func (This *Repository) GetDownloadUrl() string {
	if This.Type == REPOSITORY_TYPE_GITHUB {
		dependencyRepository, _, dependencyVersion := This.GetGitData()
		return fmt.Sprintf("https://github.com/%s/archive/%s.zip", dependencyRepository, dependencyVersion)
	}

	return ""
}

func (This *Repository) GetFileName() string {
	if This.Type == REPOSITORY_TYPE_GITHUB {
		_, _, dependencyVersion := This.GetGitData()
		return slug.Make(fmt.Sprintf("%s-%s", This.Name, dependencyVersion)) + ".zip"
	}

	return ""
}

func (This *Repository) GetDirectoryName() string {
	if This.Type == REPOSITORY_TYPE_GITHUB {
		dependencyRepository, _, dependencyVersion := This.GetGitData()
		dependencyRepositoryParts := strings.Split(dependencyRepository, "/")
		return fmt.Sprintf("%s-%s", slug.Make(dependencyRepositoryParts[1]), dependencyVersion)
	} else if This.Type == REPOSITORY_TYPE_LOCAL {
		_, file := filepath.Split(This.Name)
		return file
	}

	return ""
}

func (This *Repository) GetGitData() (string, string, string) {
	// 1 = repository name
	// 2 = git type [b = branch, t = tag, c = commit]
	// 3 = name [tag name, branch name or version name]

	re := regexp.MustCompile(`(.*\w)(:)(.*\w)`)
	groups := re.FindAllStringSubmatch(This.Version, -1)

	// if we cannot parse but has version, return the tag, else we will return branch master
	if len(groups) != 1 || len(groups[0]) != 4 {
		if len(This.Version) > 0 {
			return This.Name, GIT_REPOSITORY_TYPE_TAG, This.Version
		} else {
			return This.Name, GIT_REPOSITORY_TYPE_BRANCH, "master"
		}
	}

	// return parsed data
	dependencyName := This.Name
	dependencyType := groups[0][1]
	dependencyVersion := groups[0][3]

	return dependencyName, dependencyType, dependencyVersion
}

func (This *Repository) Prepare(processData *ProcessData) {
	if This.Type == REPOSITORY_TYPE_LOCAL {
		This.Name = processData.ParseString(This.Name)
	}
}

func (This *Repository) GetTempWorkingDir() string {
	if This.Type == REPOSITORY_TYPE_GITHUB {
		return filepath.Join(constants.TEMPORARY_DIRECTORY, This.GetDirectoryName())
	} else if This.Type == REPOSITORY_TYPE_LOCAL {
		return This.Name
	}

	return ""
}

func (This *Repository) GetFullRepositoryDir() string {
	if This.Type == REPOSITORY_TYPE_GITHUB {
		return filepath.Join(osutils.GetCurrentDir(), constants.TEMPORARY_DIRECTORY, This.GetDirectoryName())
	} else if This.Type == REPOSITORY_TYPE_LOCAL {
		return This.Name
	}

	return ""
}
