package tools

import (
	"github.com/otiai10/gosseract/v2"
)

func OCR(imageBytes []byte) (string, error) {

	client := gosseract.NewClient()
	defer client.Close()

	client.SetImageFromBytes(imageBytes)

	text, err := client.Text()
	if err != nil {
		return "", err
	}

	return text, nil
}
