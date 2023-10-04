package main

import (
	"log"
	"net/http"

	"github.com/joho/godotenv"
	"github.com/quotientbot/ocr/routers"
)

func main() {

	err := godotenv.Load()
	if err != nil {
		log.Fatal("Error loading .env file")
	}
	log.Println("Loaded .env successfully")

	mux := http.NewServeMux()
	mux.HandleFunc("/", routers.IndexHandler)
	mux.HandleFunc("/ocr", routers.OCRHandler)

	s := &http.Server{
		Addr:    "0.0.0.0:8080",
		Handler: mux,
	}

	log.Println("Listening on port 8080")
	log.Fatal(s.ListenAndServe())

}
