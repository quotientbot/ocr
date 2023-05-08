![Language](https://img.shields.io/badge/lang-Python%203.9-green)
![Library](https://img.shields.io/badge/lib-pytesseract%200.3.10-blue)
![Library](https://img.shields.io/badge/lib-FastAPI%20-gold)
![Library](https://img.shields.io/badge/lib-ImageHash%20-red)
![Library](https://img.shields.io/badge/lib-PIL%20-purple)



# OCR-API
The microservice that powers [Quotient's](https://github.com/quotientbot/Quotient-Bot/) image text extraction & image duplicacy detection needs.

## What it does?
If put simply, In response to an HTTP request containing an array of Image URLs, the API performs the following:
* Make those images sharper, remove colors, etc., and then extract whatever text they contain.
* Generate a [Perceptual](https://en.wikipedia.org/wiki/Perceptual_hashing) & [Difference hash](https://www.hackerfactor.com/blog/index.php?/archives/529-Kind-of-Like-That.html).
* In response to our request, provide us with all this data.

### Example Usage using FastAPI docs
> We are using the following image </br>
![image](https://user-images.githubusercontent.com/72350242/213885619-f49016e8-b69c-4471-924f-779e4c37b0e0.png)

> Response:
![ocr-example](https://user-images.githubusercontent.com/72350242/213885740-590c4312-a441-4f14-ac98-b8062864f5c9.png)
