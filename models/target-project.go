package models

type TargetProject struct {
	Target struct {
		Build      []string `json:"build"`
		ParseFiles []string `json:"parseFiles"`
	} `json:"target"`
}
