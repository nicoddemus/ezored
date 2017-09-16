package osutils

import (
	"bytes"
	"errors"
	"os/exec"
	"runtime"
)

func Exec(command []string, workingDirectory string, environ []string) (string, error) {
	head := command[0]
	command = command[1:]

	var stdout bytes.Buffer
	var stderr bytes.Buffer

	cmd := exec.Command(head, command...)
	cmd.Stdout = &stdout
	cmd.Stderr = &stderr
	cmd.Dir = workingDirectory
	cmd.Env = environ

	err := cmd.Run()

	if err != nil {
		if stderr.Len() > 0 {
			return "", errors.New(stderr.String())
		}

		if stdout.Len() > 0 {
			return "", errors.New(stdout.String())
		}

		return "", err
	}

	return stdout.String(), nil
}

func IsWindows() bool {
	if runtime.GOOS == "windows" {
		return true
	}

	return false
}
