export GO111MODULE=on

.PHONY: build

tidy:
	go mod tidy

build:
	docker build -t "github.com/quotientbot/ocr" .

run: tidy build
	docker run -it --rm -p 8080:8080 "github.com/quotientbot/ocr"

prod: tidy build
	git pull || true
	docker stop ocr || true
	docker rm ocr || true
	docker run -d -p 8080:8080 --name "ocr" "github.com/quotientbot/ocr"