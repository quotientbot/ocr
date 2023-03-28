from __future__ import annotations

import functools
import io
import itertools
from typing import TYPE_CHECKING, Any, Dict, List, Optional

import aiohttp
import imagehash
import pytesseract
from lru import LRU
from PIL import Image, ImageFilter

from .converters import to_async

__all__ = ("OCRImage",)

cache: "Dict[str, str]" = LRU(100)


class OCRImage:
    if TYPE_CHECKING:
        crop: Image.Image.crop
        size: Image.Image.size

    def __init__(self, img: Image.Image) -> None:
        self._img = img

    def __getattr__(self, key: str) -> Any:
        if key == "_img":
            raise AttributeError()
        return getattr(self._img, key)

    @functools.cached_property
    def dhash(self, size: int = 64) -> str:
        return str(imagehash.dhash(self, size))

    @functools.cached_property
    def phash(self, size: int = 64) -> str:
        return str(imagehash.phash(self, size))

    @staticmethod
    async def from_url(url: str) -> Optional[OCRImage]:
        async with aiohttp.ClientSession() as session:
            resp = await session.post(url)
            if resp.status != 200:
                return None

            return OCRImage(Image.open(io.BytesIO(await resp.read())).convert("L").filter(ImageFilter.SHARPEN))

    async def get_text(self) -> str:
        try:
            return cache[self.dhash]
        except KeyError:
            return await self.__run_ocr()

    @to_async()
    def __run_ocr(self) -> str:
        images: List[Image.Image] = self.__image_slices()

        images.append(self)
        t = ""

        for image in images:
            w, h = image.size
            image = image.resize((w * 3, h * 3)).filter(ImageFilter.SHARPEN)

            try:
                t += pytesseract.image_to_string(image, lang="eng", config="--oem 3 --psm 12")
            except pytesseract.TesseractError:
                continue

        cache[self.dhash] = t
        return t

    def __image_slices(self, height: int = 400) -> List[Image.Image]:
        list_of_images: List[Image.Image] = []
        imgwidth, imgheight = self.size
        for i, j in itertools.product(range(imgheight // height), range(imgwidth // imgwidth)):
            box = (j * imgwidth, i * height, (j + 1) * imgwidth, (i + 1) * height)
            list_of_images.append(self.crop(box))

        return list_of_images
