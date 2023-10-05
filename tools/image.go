package tools

import (
	"fmt"
	"io"
	"net/http"
	"net/url"
)

func GetBytesFromURL(imageURL string) ([]byte, error) {

	parsedURL, err := url.Parse(imageURL)
	if err != nil {
		return nil, err
	}
	// Remove query parameters
	parsedURL.RawQuery = ""

	// Reconstruct the cleaned URL
	cleanedURL := parsedURL.String()
	resp, err := http.Get(cleanedURL)

	fmt.Println("cleanedURL: ", cleanedURL)

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
