EXECUTABLE=ezored
LOG_FILE=/var/log/${EXECUTABLE}.log
GOFMT=gofmt -w
GODEPS=go get -u
PACKAGE=github.com/ezored/ezored

.DEFAULT_GOAL := help

help:
	@echo "Type: make [rule]. Available options are:"
	@echo ""
	@echo "- help"
	@echo "- build"
	@echo "- install"
	@echo "- format"
	@echo "- deps"
	@echo "- test"
	@echo "- build-all"
	@echo "- generate-bindata"
	@echo ""

build:
	go build -o ${EXECUTABLE}

install:
	go install

format:
	${GOFMT} main.go
	${GOFMT} commands/base-command.go
	${GOFMT} commands/clean-command.go
	${GOFMT} commands/build-command.go
	${GOFMT} commands/dependency-command.go
	${GOFMT} commands/help-command.go
	${GOFMT} commands/init-command.go
	${GOFMT} constants/constants.go
	${GOFMT} logger/logger.go
	${GOFMT} models/copy-file.go
	${GOFMT} models/project.go
	${GOFMT} models/repository.go
	${GOFMT} models/vendor.go
	${GOFMT} utils/file-utils/file-utils.go
	${GOFMT} utils/flag-utils/flag-utils.go
	${GOFMT} utils/os-utils/os-utils.go

test:

deps:
	${GODEPS} github.com/gosimple/slug

update:
	git pull origin master
	make install

generate-bindata:
	go-bindata -o assets/bindata.go -pkg assets -ignore=.gitignore -ignore .DS_Store bindata/...

build-all:
	rm -rf build

	mkdir -p build/linux32
	env GOOS=linux GOARCH=386 go build -o build/linux32/${EXECUTABLE} -v ${PACKAGE}

	mkdir -p build/linux64
	env GOOS=linux GOARCH=amd64 go build -o build/linux64/${EXECUTABLE} -v ${PACKAGE}

	mkdir -p build/darwin64
	env GOOS=darwin GOARCH=amd64 go build -o build/darwin64/${EXECUTABLE} -v ${PACKAGE}

	mkdir -p build/windows32
	env GOOS=windows GOARCH=386 go build -o build/windows32/${EXECUTABLE}.exe -v ${PACKAGE}

	mkdir -p build/windows64
	env GOOS=windows GOARCH=amd64 go build -o build/windows64/${EXECUTABLE}.exe -v ${PACKAGE}