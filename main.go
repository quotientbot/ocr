package main

import (
	"context"
	"fmt"
	"os"

	"github.com/aws/aws-lambda-go/lambda"
	"github.com/otiai10/gosseract/v2"
)

type Response struct {
	Body       string `json:"body"`
	StatusCode int    `json:"statusCode"`
}
type Request struct {
	Image string `json:"image"`
}

func generateResponse(ImageURL string, Code int) Response {
	client := gosseract.NewClient()
	defer client.Close()

	client.SetImage(ImageURL)
	text, err := client.Text()
	if err != nil {
		return Response{Body: err.Error(), StatusCode: 500}
	}
	return Response{Body: text, StatusCode: Code}
}

func handleRequest(_ context.Context, request Request) (Response, error) {
	// Debugging: Print working directory
	pwd, _ := os.Getwd()
	fmt.Println("Current working directory:", pwd)

	// Set LD_LIBRARY_PATH
	os.Setenv("LD_LIBRARY_PATH", "/opt/lib")

	// Debugging: List files in library directory
	files, _ := os.ReadDir("/opt/lib")
	for _, f := range files {
		fmt.Println(f.Name())
	}

	return generateResponse(request.Image, 200), nil
}

func main() {
	lambda.Start(handleRequest)
}
