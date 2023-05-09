![Language](https://img.shields.io/badge/lang-Python%203.8-green)
![Library](https://img.shields.io/badge/lib-pytesseract%200.3.10-blue)
![Library](https://img.shields.io/badge/lib-FastAPI%20-gold)
![Library](https://img.shields.io/badge/lib-ImageHash%20-red)
![Library](https://img.shields.io/badge/lib-Pillow%20-purple)

# OCR-API

This is a standalone API designed to verify the authenticity of submitted screenshots in esports servers, for scrims or tourney registrations. The API extracts text from the screenshots sent by users and generates hash data which is then used to check the authenticity of the screenshot and to determine if the screenshots have already been submitted by other users.

> This microservice powers [Quotient's](https://github.com/quotientbot/Quotient-Bot/) ssverification feature.

This API is built to work exclusively with Discord attachments URLs that are images. In response to an HTTP request containing an array of Discord attachment URLs, the API performs the following:

- Sharpens the images, removes colors, and extracts whatever text they contain using `Tesseract`.
- Generates a [Perceptual](https://en.wikipedia.org/wiki/Perceptual_hashing) & [Difference hash](https://www.hackerfactor.com/blog/index.php?/archives/529-Kind-of-Like-That.html).
- Provides all this data in response to our request.

## Dependencies:

- [`fastapi`](https://pypi.org/project/fastapi/) - A modern, fast (high-performance), web framework for building APIs.
- [`pytesseract`](https://pypi.org/project/pytesseract/) - A wrapper for Google’s Tesseract-OCR Engine.
- [`Pillow`](https://pypi.org/project/Pillow/) - Python Imaging Library.
- [`ImageHash`](https://pypi.org/project/ImageHash/) - An image hashing library written in Python.
- [`aiohttp`](https://pypi.org/project/aiohttp) - Asynchronous HTTP Client/Server for asyncio
- [`python-decouple`](https://pypi.org/project/python-decouple/) - An independent generic tool for separating settings from code.
- [`uvicorn`](https://pypi.org/project/uvicorn/) - An ASGI web server implementation for Python.
- [`lru-dict`](https://pypi.org/project/lru-dict/) - A fixed size dict like container which evicts Least Recently Used (LRU) items once size limit is exceeded.

## Example Usage using Swagger UI
> Psst! Are you one of the secret agents from the organization I applied to? Welcome! To test out this app, head over to https://quotientbot.xyz/ocr/docs. But shh... the secret key you'll need is a top-secret code. It's actually the capital short form of the organization's name. Don't tell anyone I told you! And remember this only works for Discord URLs.

We are using the following image </br>
![image](https://user-images.githubusercontent.com/72350242/213885619-f49016e8-b69c-4471-924f-779e4c37b0e0.png)

Response: ![ocr-example](https://user-images.githubusercontent.com/72350242/213885740-590c4312-a441-4f14-ac98-b8062864f5c9.png)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
