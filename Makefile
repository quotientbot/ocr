export GO111MODULE=on

.PHONY: build

pull:
	git pull

tidy:
	go mod tidy

build:
	docker build -t "github.com/quotientbot/ocr" .

run: build # when running locally, use this.
	docker run -it --rm -p 8080:8080 "github.com/quotientbot/ocr"

local: tidy run # requires go 1.11+

prod: pull build
	docker stop ocr || true
	docker rm ocr || true
	docker run -d -p 8080:8080 --restart unless-stopped --name "ocr" "github.com/quotientbot/ocr"