// Code generated by go-bindata.
// sources:
// bindata/init-command/ezored-project.json
// DO NOT EDIT!

package assets

import (
	"bytes"
	"compress/gzip"
	"fmt"
	"io"
	"io/ioutil"
	"os"
	"path/filepath"
	"strings"
	"time"
)

func bindataRead(data []byte, name string) ([]byte, error) {
	gz, err := gzip.NewReader(bytes.NewBuffer(data))
	if err != nil {
		return nil, fmt.Errorf("Read %q: %v", name, err)
	}

	var buf bytes.Buffer
	_, err = io.Copy(&buf, gz)
	clErr := gz.Close()

	if err != nil {
		return nil, fmt.Errorf("Read %q: %v", name, err)
	}
	if clErr != nil {
		return nil, err
	}

	return buf.Bytes(), nil
}

type asset struct {
	bytes []byte
	info  os.FileInfo
}

type bindataFileInfo struct {
	name    string
	size    int64
	mode    os.FileMode
	modTime time.Time
}

func (fi bindataFileInfo) Name() string {
	return fi.name
}
func (fi bindataFileInfo) Size() int64 {
	return fi.size
}
func (fi bindataFileInfo) Mode() os.FileMode {
	return fi.mode
}
func (fi bindataFileInfo) ModTime() time.Time {
	return fi.modTime
}
func (fi bindataFileInfo) IsDir() bool {
	return false
}
func (fi bindataFileInfo) Sys() interface{} {
	return nil
}

var _bindataInitCommandEzoredProjectJson = []byte("\x1f\x8b\x08\x00\x00\x00\x00\x00\x00\xff\x9c\x90\x31\x4f\xf3\x30\x10\x86\x67\xfb\x57\x54\x9e\xdb\x7c\xed\x37\xa1\x6e\x40\x5b\x28\x13\x52\xd9\x50\x07\x27\x3e\xd2\x43\xf1\xd9\x72\xdc\x48\xa1\xea\x7f\x47\xb6\x93\x40\x45\x18\xe8\x7a\xf7\xdc\xdd\x73\xef\x89\x33\x51\x18\x7a\xc3\x52\x2c\x27\x27\xce\x98\x20\xa9\x41\x2c\x27\x62\xfd\x61\x1c\x28\x31\x0d\x35\x34\x75\xd7\x66\x42\x41\x03\x95\xb1\x1a\xc8\xbf\x80\xd4\x5b\x15\xe0\xdb\xbb\xfb\xd5\x7a\xf3\xf0\xb8\x7d\x8a\x03\x4c\xe4\x47\x52\x15\xa4\x66\x61\x74\x06\x71\x5b\x56\x61\xee\xa4\x6b\x3b\xa8\x30\x0a\x76\x58\xd2\x56\x01\x79\xf4\x6d\x80\xf1\xf9\x60\x08\x26\xab\x74\x05\x5c\x87\x2a\xb0\x95\x69\xe3\x51\xe9\x4a\xf0\x01\xbd\xc9\xe6\x43\xb7\xc1\x02\x36\x52\x63\x15\x97\x2c\xa6\xff\xbb\x4e\x03\xae\x46\x43\xb1\x98\xcd\x87\x81\xc2\xda\x9d\x97\xa4\xa4\x8b\x86\x8b\x85\xe0\x8c\x9d\xe3\xaf\x92\x94\x33\xa8\x86\x7f\xc7\x51\x1e\x69\xe1\xa3\x4c\x08\xe7\x95\x33\x96\x06\xfa\x00\x43\x68\xe9\x9a\x03\x6b\x6a\xf4\xc6\xb5\xfd\xd6\x2f\x2a\x05\xf3\x2f\x2d\x9a\x0d\x33\x4c\xf8\xd6\x46\xa0\x44\x7f\x38\xe6\x7d\xf5\xdb\x3f\xf9\x52\xcb\xda\x83\x0b\x3e\x41\x28\xf9\x5f\x3a\xf4\xcf\xfc\xd5\xe3\x62\xee\x2a\x17\xce\xf6\x21\x20\x05\x16\x48\x01\x15\x08\xe3\x29\x75\x77\x07\xae\x9d\xa9\x77\x24\xc2\x59\x7d\xb4\xd6\x38\xdf\xa9\x8f\x19\xfc\x26\x30\x92\xc3\xcf\x2b\xb5\xd4\xb6\x82\x6b\xb6\x73\xb6\xe7\xe7\xcf\x00\x00\x00\xff\xff\x60\x0b\x46\xa1\x38\x03\x00\x00")

func bindataInitCommandEzoredProjectJsonBytes() ([]byte, error) {
	return bindataRead(
		_bindataInitCommandEzoredProjectJson,
		"bindata/init-command/ezored-project.json",
	)
}

func bindataInitCommandEzoredProjectJson() (*asset, error) {
	bytes, err := bindataInitCommandEzoredProjectJsonBytes()
	if err != nil {
		return nil, err
	}

	info := bindataFileInfo{name: "bindata/init-command/ezored-project.json", size: 824, mode: os.FileMode(420), modTime: time.Unix(1506795615, 0)}
	a := &asset{bytes: bytes, info: info}
	return a, nil
}

// Asset loads and returns the asset for the given name.
// It returns an error if the asset could not be found or
// could not be loaded.
func Asset(name string) ([]byte, error) {
	cannonicalName := strings.Replace(name, "\\", "/", -1)
	if f, ok := _bindata[cannonicalName]; ok {
		a, err := f()
		if err != nil {
			return nil, fmt.Errorf("Asset %s can't read by error: %v", name, err)
		}
		return a.bytes, nil
	}
	return nil, fmt.Errorf("Asset %s not found", name)
}

// MustAsset is like Asset but panics when Asset would return an error.
// It simplifies safe initialization of global variables.
func MustAsset(name string) []byte {
	a, err := Asset(name)
	if err != nil {
		panic("asset: Asset(" + name + "): " + err.Error())
	}

	return a
}

// AssetInfo loads and returns the asset info for the given name.
// It returns an error if the asset could not be found or
// could not be loaded.
func AssetInfo(name string) (os.FileInfo, error) {
	cannonicalName := strings.Replace(name, "\\", "/", -1)
	if f, ok := _bindata[cannonicalName]; ok {
		a, err := f()
		if err != nil {
			return nil, fmt.Errorf("AssetInfo %s can't read by error: %v", name, err)
		}
		return a.info, nil
	}
	return nil, fmt.Errorf("AssetInfo %s not found", name)
}

// AssetNames returns the names of the assets.
func AssetNames() []string {
	names := make([]string, 0, len(_bindata))
	for name := range _bindata {
		names = append(names, name)
	}
	return names
}

// _bindata is a table, holding each asset generator, mapped to its name.
var _bindata = map[string]func() (*asset, error){
	"bindata/init-command/ezored-project.json": bindataInitCommandEzoredProjectJson,
}

// AssetDir returns the file names below a certain
// directory embedded in the file by go-bindata.
// For example if you run go-bindata on data/... and data contains the
// following hierarchy:
//     data/
//       foo.txt
//       img/
//         a.png
//         b.png
// then AssetDir("data") would return []string{"foo.txt", "img"}
// AssetDir("data/img") would return []string{"a.png", "b.png"}
// AssetDir("foo.txt") and AssetDir("notexist") would return an error
// AssetDir("") will return []string{"data"}.
func AssetDir(name string) ([]string, error) {
	node := _bintree
	if len(name) != 0 {
		cannonicalName := strings.Replace(name, "\\", "/", -1)
		pathList := strings.Split(cannonicalName, "/")
		for _, p := range pathList {
			node = node.Children[p]
			if node == nil {
				return nil, fmt.Errorf("Asset %s not found", name)
			}
		}
	}
	if node.Func != nil {
		return nil, fmt.Errorf("Asset %s not found", name)
	}
	rv := make([]string, 0, len(node.Children))
	for childName := range node.Children {
		rv = append(rv, childName)
	}
	return rv, nil
}

type bintree struct {
	Func     func() (*asset, error)
	Children map[string]*bintree
}
var _bintree = &bintree{nil, map[string]*bintree{
	"bindata": &bintree{nil, map[string]*bintree{
		"init-command": &bintree{nil, map[string]*bintree{
			"ezored-project.json": &bintree{bindataInitCommandEzoredProjectJson, map[string]*bintree{}},
		}},
	}},
}}

// RestoreAsset restores an asset under the given directory
func RestoreAsset(dir, name string) error {
	data, err := Asset(name)
	if err != nil {
		return err
	}
	info, err := AssetInfo(name)
	if err != nil {
		return err
	}
	err = os.MkdirAll(_filePath(dir, filepath.Dir(name)), os.FileMode(0755))
	if err != nil {
		return err
	}
	err = ioutil.WriteFile(_filePath(dir, name), data, info.Mode())
	if err != nil {
		return err
	}
	err = os.Chtimes(_filePath(dir, name), info.ModTime(), info.ModTime())
	if err != nil {
		return err
	}
	return nil
}

// RestoreAssets restores an asset under the given directory recursively
func RestoreAssets(dir, name string) error {
	children, err := AssetDir(name)
	// File
	if err != nil {
		return RestoreAsset(dir, name)
	}
	// Dir
	for _, child := range children {
		err = RestoreAssets(dir, filepath.Join(name, child))
		if err != nil {
			return err
		}
	}
	return nil
}

func _filePath(dir, name string) string {
	cannonicalName := strings.Replace(name, "\\", "/", -1)
	return filepath.Join(append([]string{dir}, strings.Split(cannonicalName, "/")...)...)
}

