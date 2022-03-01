from __future__ import annotations


import imagehash
import pytesseract
import io
import aiohttp

from PIL import Image

from ._const import SS
from src.utils import ToAsync


async def get_image(attch: SS) -> Image:
    async with aiohttp.ClientSession() as session:
        resp = await session.post(attch.url)
        if resp.status != 200:
            return None

        return Image.open(io.BytesIO(await resp.read()))


def slice_image(img, height: int = 400):
    _l = []
    imgwidth, imgheight = img.size
    for i in range(imgheight // height):
        for j in range(imgwidth // imgwidth):
            box = (j * imgwidth, i * height, (j + 1) * imgwidth, (i + 1) * height)
            _l.append(img.crop(box))

    return _l


@ToAsync()
def get_image_string(img):

    _img = img.convert("L")

    cropped = slice_image(_img)
    cropped.append(_img)

    text = ""
    config = "--oem 3 --psm 12"

    for _ in cropped:
        width, height = _.size
        _ = _.resize((width * 3, height * 3))

        text += pytesseract.image_to_string(img, lang="eng", config=config)

    return text


@ToAsync()
def get_image_dhash(img, size=64):
    return imagehash.dhash(img, size)


@ToAsync()
def get_image_phash(img, size=64):
    return imagehash.phash(img, size)