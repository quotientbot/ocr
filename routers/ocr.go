package routers

import (
	"encoding/json"
	"net/http"
	"os"

	"github.com/quotientbot/ocr/tools"
)

type Images struct {
	ImageURLs []string `json:"urls"`
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

	var imgs Images
	if err := json.NewDecoder(r.Body).Decode(&imgs); err != nil {
		w.WriteHeader(http.StatusBadRequest)
		return
	}

	result := make([]map[string]string, 0)

	for _, imageURL := range imgs.ImageURLs {
		imageBytes, err := tools.GetBytesFromURL(imageURL)
		if err != nil {
			continue
		}

		text, dhash, phash, err := tools.OCR(imageBytes)
		if err != nil {
			continue
		}

		res := map[string]string{"url": imageURL, "dhash": dhash[2:], "phash": phash[2:], "text": text}
		result = append(result, res)
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(result)
}
