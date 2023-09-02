package tools

import (
	"io"
	"net/http"
)

func GetBytesFromURL(imageURL string) ([]byte, error) {

	resp, err := http.Get(imageURL)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	imageBytes, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}

	return imageBytes, nil
}
