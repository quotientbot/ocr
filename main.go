package main

import (
	"context"

	"github.com/aws/aws-lambda-go/events"
	"github.com/aws/aws-lambda-go/lambda"
)

type Response events.APIGatewayProxyResponse

func generateResponse(Body string, Code int) Response {
	return Response{Body: Body, StatusCode: Code}
}
func handleRequest(_ context.Context, request events.LambdaFunctionURLRequest) (Response, error) {
	return generateResponse("Hello World!", 200), nil
}
func main() {
	lambda.Start(handleRequest)
}
