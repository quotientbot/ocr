export GO111MODULE=on

.PHONY: tidy build

tidy:
	go mod tidy

build:
	env CGO_ENABLED=1 GOOS=linux GOARCH=amd64  go build  -o bin/ocr .

test-prod: tidy build
	sls invoke -f ocr --path event.json

test-local: tidy build
	sls invoke local -f ocr --path event.json 

deploy: tidy build
	sls deploy --verbose