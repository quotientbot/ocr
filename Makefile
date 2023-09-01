export GO111MODULE=on

.PHONY: build

tidy:
	go mod tidy

build:
	go build  -o bin/ocr .

run: tidy
	go run .
