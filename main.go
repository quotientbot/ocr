package main

import (
	"context"

	"github.com/aws/aws-lambda-go/lambda"
)

type Response struct {
	Body       string `json:"body"`
	StatusCode int    `json:"statusCode"`
}
type Request struct {
	Image string `json:"image"`
}

func generateResponse(Body string, Code int) Response {
	return Response{Body: Body, StatusCode: Code}
}

func handleRequest(_ context.Context, request Request) (Response, error) {
	return generateResponse(request.Image, 200), nil
}
func main() {
	lambda.Start(handleRequest)
}
