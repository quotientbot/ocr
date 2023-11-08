export GO111MODULE=on

.PHONY: build

pull:
	git pull

tidy:
	go mod tidy

build:
	docker build -t "github.com/quotientbot/ocr" .

run: tidy build # when running locally, use this
	docker run -it --rm -p 8080:8080 "github.com/quotientbot/ocr"

prod: pull build
	docker stop ocr || true
	docker rm ocr || true
	docker run -d -p 8080:8080 --restart unless-stopped --name "ocr" "github.com/quotientbot/ocr"