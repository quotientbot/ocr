export GO111MODULE=on

.PHONY: build

tidy:
	go mod tidy

build:
	docker build -t "github.com/quotientbot/ocr" .

run: tidy build
	docker run -it --rm -p 8080:8080 "github.com/quotientbot/ocr"