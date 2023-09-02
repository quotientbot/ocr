package routers

import (
	"encoding/json"
	"net/http"

	"github.com/otiai10/gosseract/v2"
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

	client := gosseract.NewClient()
	defer client.Close()

	client.SetImageFromBytes(imageBytes)

	text, err := client.Text()
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		// log.Fatal(err)

	}

	res := map[string]string{"image": img.ImageURL, "text": text}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(res)
}
