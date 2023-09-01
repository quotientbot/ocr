package main

import (
	"log"
	"net/http"

	"github.com/quotientbot/ocr/routers"
)

func main() {
	mux := http.NewServeMux()
	mux.HandleFunc("/", routers.IndexHandler)
	mux.HandleFunc("/ocr", routers.OCRHandler)

	
	s := &http.Server{
		Addr:    ":8080",
		Handler: mux,
	}

	log.Fatal(s.ListenAndServe())

}
