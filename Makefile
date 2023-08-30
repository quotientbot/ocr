export GO111MODULE=on

.PHONY: tidy build

tidy:
	go mod tidy

build:
	env CGO_ENABLED=0 GOOS=linux GOARCH=amd64  go build  -o bin/ocr .

deploy: tidy build
	sls deploy --verbose