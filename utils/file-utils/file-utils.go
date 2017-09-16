package fileutils

import (
	"archive/zip"
	"encoding/json"
	"fmt"
	"github.com/ezored/ezored/assets"
	"github.com/ezored/ezored/constants"
	"github.com/ezored/ezored/logger"
	"github.com/ezored/ezored/models"
	"io"
	"io/ioutil"
	"net/http"
	"os"
	"path/filepath"
)

func CreateFileWithContent(directory string, filename string, content []byte) {
	os.MkdirAll(directory, constants.DIRECTORY_PERMISSIONS)

	err := ioutil.WriteFile(filepath.Join(directory, filename), content, constants.FILE_PERMISSIONS)

	if err != nil {
		logger.F(err.Error())
	}
}

func Exists(filePath string) bool {
	if _, err := os.Stat(filePath); !os.IsNotExist(err) {
		return true
	}

	return false
}

func CreateDependenciesDirectory() {
	os.Mkdir(constants.DEPENDENCIES_DIRECTORY, constants.DIRECTORY_PERMISSIONS)
}

func CreateTemporaryDirectory() {
	os.Mkdir(constants.TEMPORARY_DIRECTORY, constants.DIRECTORY_PERMISSIONS)
}

func CreateBuildDirectory() {
	os.Mkdir(constants.BUILD_DIRECTORY, constants.DIRECTORY_PERMISSIONS)
}

func DownloadFile(filepath string, url string) (err error) {
	// create the file
	out, err := os.Create(filepath)

	if err != nil {
		return err
	}

	defer out.Close()

	// get the data
	resp, err := http.Get(url)

	if err != nil {
		return err
	}

	defer resp.Body.Close()

	// writer the body to file
	_, err = io.Copy(out, resp.Body)

	if err != nil {
		return err
	}

	return nil
}

func Unzip(src, dest string) error {
	r, err := zip.OpenReader(src)

	if err != nil {
		return err
	}

	defer func() {
		if err := r.Close(); err != nil {
			panic(err)
		}
	}()

	os.MkdirAll(dest, 0755)

	// closure to address file descriptors issue with all the deferred .Close() methods
	extractAndWriteFile := func(f *zip.File) error {
		rc, err := f.Open()

		if err != nil {
			return err
		}

		defer func() {
			if err := rc.Close(); err != nil {
				panic(err)
			}
		}()

		path := filepath.Join(dest, f.Name)

		if f.FileInfo().IsDir() {
			os.MkdirAll(path, f.Mode())
		} else {
			os.MkdirAll(filepath.Dir(path), f.Mode())
			f, err := os.OpenFile(path, os.O_WRONLY|os.O_CREATE|os.O_TRUNC, f.Mode())

			if err != nil {
				return err
			}

			defer func() {
				if err := f.Close(); err != nil {
					panic(err)
				}
			}()

			_, err = io.Copy(f, rc)

			if err != nil {
				return err
			}
		}

		return nil
	}

	for _, f := range r.File {
		err := extractAndWriteFile(f)

		if err != nil {
			return err
		}
	}

	return nil
}

func GetAssetContent(assetName string) []byte {
	content, _ := assets.Asset(assetName)
	return content
}

func IsDirectory(path string) (bool, error) {
	fileInfo, err := os.Stat(path)

	if err != nil {
		return false, err
	}

	return fileInfo.IsDir(), nil
}

func CopyAllFiles(copyFiles []models.CopyFile) {
	for _, copyFile := range copyFiles {
		isDir, err := IsDirectory(copyFile.From)

		if err != nil {
			logger.F(err.Error())
		}

		if isDir {
			CopyDir(copyFile.From, copyFile.To)
		} else {
			CopyFile(copyFile.From, copyFile.To)
		}
	}
}

func CopyFile(src, dst string) (err error) {
	in, err := os.Open(src)

	if err != nil {
		return
	}

	srcDir := filepath.Dir(src)
	srcDirStat, err := os.Stat(srcDir)

	if err != nil {
		return
	}

	destDir := filepath.Dir(dst)
	os.MkdirAll(destDir, srcDirStat.Mode())

	defer in.Close()

	out, err := os.Create(dst)

	if err != nil {
		return
	}

	defer func() {
		if e := out.Close(); e != nil {
			err = e
		}
	}()

	_, err = io.Copy(out, in)

	if err != nil {
		return
	}

	err = out.Sync()

	if err != nil {
		return
	}

	si, err := os.Stat(src)

	if err != nil {
		return
	}

	err = os.Chmod(dst, si.Mode())

	if err != nil {
		return
	}

	return
}

func CopyDir(src string, dst string) (err error) {
	src = filepath.Clean(src)
	dst = filepath.Clean(dst)

	si, err := os.Stat(src)

	if err != nil {
		return err
	}

	if !si.IsDir() {
		return fmt.Errorf("source is not a directory")
	}

	_, err = os.Stat(dst)

	if err != nil && !os.IsNotExist(err) {
		return
	}

	if err == nil {
		return fmt.Errorf("destination already exists")
	}

	err = os.MkdirAll(dst, si.Mode())

	if err != nil {
		return
	}

	entries, err := ioutil.ReadDir(src)

	if err != nil {
		return
	}

	for _, entry := range entries {
		srcPath := filepath.Join(src, entry.Name())
		dstPath := filepath.Join(dst, entry.Name())

		if entry.IsDir() {
			err = CopyDir(srcPath, dstPath)

			if err != nil {
				return
			}
		} else {
			// Skip symlinks.
			if entry.Mode()&os.ModeSymlink != 0 {
				continue
			}

			err = CopyFile(srcPath, dstPath)

			if err != nil {
				return
			}
		}
	}

	return
}

func GetProject() models.Project {
	// we dont return error, we want throw error here, because it never can happen
	fileContent, err := ioutil.ReadFile(constants.PROJECT_FILENAME)

	if err != nil {
		logger.F(err.Error())
	}

	var project models.Project
	err = json.Unmarshal(fileContent, &project)

	if err != nil {
		logger.F(err.Error())
	}

	return project
}
