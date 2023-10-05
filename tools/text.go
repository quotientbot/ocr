package tools

import (
	"bytes"
	"image"
	"image/color"
	"image/jpeg"
	"image/png"

	"github.com/corona10/goimagehash"
	"github.com/otiai10/gosseract/v2"
)

func ConvertToBlackAndWhite(img image.Image) image.Image {
	// Create a new image with the same dimensions as the input image
	bounds := img.Bounds()
	bwImg := image.NewGray(bounds)

	// Iterate through each pixel and convert it to grayscale
	for x := bounds.Min.X; x < bounds.Max.X; x++ {
		for y := bounds.Min.Y; y < bounds.Max.Y; y++ {
			oldColor := img.At(x, y)
			grayColor := color.GrayModel.Convert(oldColor)
			bwImg.Set(x, y, grayColor)
		}
	}

	return bwImg
}

func OCR(imageBytes []byte) (string, string, string, error) {
	// Decode the imageBytes to an image.Image
	img, format, err := image.Decode(bytes.NewReader(imageBytes))
	if err != nil {
		return "", "", "", err
	}

	// Perform preprocessing: Convert to black and white
	bwImg := ConvertToBlackAndWhite(img)

	phash, err := goimagehash.ExtPerceptionHash(img, 64, 64)

	dhash, err := goimagehash.ExtDifferenceHash(img, 64, 64)

	// Encode the preprocessed image back to bytes
	var preprocessedImageBuf bytes.Buffer

	if format == "jpeg" {
		err = jpeg.Encode(&preprocessedImageBuf, bwImg, nil)
	} else {
		err = png.Encode(&preprocessedImageBuf, bwImg)
	}
	if err != nil {
		return "", "", "", err
	}

	client := gosseract.NewClient()
	defer client.Close()
	// Set the preprocessed image as the input for OCR
	client.SetImageFromBytes(preprocessedImageBuf.Bytes())

	// Perform OCR on the preprocessed image
	text, err := client.Text()
	if err != nil {
		return "", "", "", err
	}

	return text, dhash.ToString(), phash.ToString(), nil
}
