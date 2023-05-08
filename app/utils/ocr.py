from PIL import Image, ImageFilter

import imagehash
import functools
import io
import aiohttp

from .converters import to_async
from lru import LRU

import pytesseract

__all__ = ("OCRImage",)

cache = LRU(100)


class OCRImage:
    def __init__(self, img):
        self._img = img

    def __getattr__(self, key):
        if key == "_img":
            raise AttributeError()
        return getattr(self._img, key)

    @functools.cached_property
    def dhash(self, size=64):
        return imagehash.dhash(self, size).__str__()

    @functools.cached_property
    def phash(self, size=64):
        return imagehash.phash(self, size).__str__()

    @staticmethod
    async def from_url(url: str):
        async with aiohttp.ClientSession() as session:
            resp = await session.post(url)
            if resp.status != 200:
                return None

            return OCRImage(Image.open(io.BytesIO(await resp.read())).convert("L").filter(ImageFilter.SHARPEN))

    async def get_text(self):
        if t := cache.get(self.dhash):
            return t

        return await self.__run_ocr()

    @to_async()
    def __run_ocr(self):

        _imges = self.__image_slices()

        _imges.append(self)
        t = ""

        for _ in _imges:
            w, h = _.size
            _ = _.resize((w * 3, h * 3)).filter(ImageFilter.SHARPEN)

            try:
                t += pytesseract.image_to_string(_, lang="eng", config="--oem 3 --psm 12")
            except pytesseract.TesseractError:
                continue

        cache[self.dhash] = t
        return t

    def __image_slices(self, height: int = 400):
        _l = []
        imgwidth, imgheight = self.size
        for i in range(imgheight // height):
            for j in range(imgwidth // imgwidth):
                box = (j * imgwidth, i * height, (j + 1) * imgwidth, (i + 1) * height)
                _l.append(self.crop(box))

        return _l
