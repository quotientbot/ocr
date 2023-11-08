# OCR-API
The microservice that powers [Quotient's](https://github.com/quotientbot/Quotient-Bot/) image text extraction & image duplicacy detection needs.

## What it does?
If put simply, In response to an HTTP request containing an array of Image URLs, the API performs the following:
* Make those images sharper, remove colors, etc., and then extract whatever text they contain.
* Generate a [Perceptual](https://en.wikipedia.org/wiki/Perceptual_hashing) & [Difference hash](https://www.hackerfactor.com/blog/index.php?/archives/529-Kind-of-Like-That.html) for the images.

> In response to a valid HTTP Post request, a similar response to the following example is expected.

### Example Usage
> We are using the following image </br>
![image](https://user-images.githubusercontent.com/72350242/213885619-f49016e8-b69c-4471-924f-779e4c37b0e0.png)

> Response:
![ocr-example](https://user-images.githubusercontent.com/72350242/213885740-590c4312-a441-4f14-ac98-b8062864f5c9.png)

## Want to run a local instance?
> Make sure you have [Docker](https://docs.docker.com/get-docker/) installed on your machine.

* Clone the repository.
* Rename the `.example.env` file to `.env` and fill in the required values.
* Run `make run` command in the root directory of the repository.
* This should start up an instance on `localhost:8080`.

## License
This project is licensed under the MPL-2.0 license - see the [LICENSE](LICENSE) file for details.
___
### Contributors 👥
<a href="https://github.com/quotientbot/Quotient-Bot/graphs/contributors">

