package models

import (
	"errors"
	"fmt"
)

type Project struct {
	Config       map[string]interface{}
	Targets      []*ProjectTarget `json:"targets"`
	Dependencies []*Repository    `json:"dependencies"`
}

type ProjectConfig struct {
	Name string `json:"name"`
}

type ProjectTarget struct {
	Name       string     `json:"name"`
	Repository Repository `json:"repository"`
}

func (This *Project) HasTargets() bool {
	if This.Targets == nil {
		return false
	}

	return len(This.Targets) > 0
}

func (This *Project) HasDependencies() bool {
	if This.Dependencies == nil {
		return false
	}

	return len(This.Dependencies) > 0
}

func (This *Project) GetConfigValue(key string) (interface{}, error) {
	if This.Config == nil {
		return nil, errors.New("no configuration data")
	}

	value, ok := This.Config[key]

	if ok {
		return value, nil
	}

	return nil, errors.New("invalid data")
}

func (This *Project) GetConfigValueAsString(key string) string {
	value, err := This.GetConfigValue(key)

	if err != nil {
		return ""
	}

	return fmt.Sprintf("%v", value)
}
