package routers

import (
	"encoding/json"
	"net/http"
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

	res := map[string]string{"image": img.ImageURL}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(res)
}
