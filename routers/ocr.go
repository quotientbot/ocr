package routers

import (
	"encoding/json"
	"net/http"
	"os"

	"github.com/quotientbot/ocr/tools"
)

type Image struct {
	ImageURL string `json:"image"`
}

func OCRHandler(w http.ResponseWriter, r *http.Request) {

	if r.Method != http.MethodPost {
		w.WriteHeader(http.StatusMethodNotAllowed)
		return
	}

	// Check the Authorization header for the secret key
	secretKey := os.Getenv("SECRET_KEY")

	authHeader := r.Header.Get("Authorization")
	if authHeader != "Bearer "+secretKey {
		w.WriteHeader(http.StatusUnauthorized)
		return
	}

	var img Image
	if err := json.NewDecoder(r.Body).Decode(&img); err != nil {
		w.WriteHeader(http.StatusBadRequest)
		return
	}

	imageBytes, err := tools.GetBytesFromURL(img.ImageURL)
	if err != nil {
		w.WriteHeader(http.StatusBadRequest)
		return
	}

	text, dhash, phash, err := tools.OCR(imageBytes)
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		// log.Fatal(err)

	}
	res := map[string]string{"url": img.ImageURL, "dhash": dhash, "phash": phash, "text": text}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(res)
}
