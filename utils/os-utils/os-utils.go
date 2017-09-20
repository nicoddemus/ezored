package osutils

import (
	"bytes"
	"errors"
	"github.com/ezored/ezored/logger"
	"os"
	"os/exec"
	"path/filepath"
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

func GetCurrentDir() string {
	dir, err := filepath.Abs(filepath.Dir(os.Args[0]))

	if err != nil {
		logger.F(err.Error())
	}

	return dir
}
