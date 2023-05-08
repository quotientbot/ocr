from PIL import Image, ImageFilter

import imagehash
import functools
import io
import aiohttp
from typing import List

from .converters import to_async
from lru import LRU

import pytesseract

__all__ = ("OCRImage",)

# A Least Recently Used (LRU) cache to store the OCR results for images
cache = LRU(100)


class OCRImage:
    def __init__(self, img: Image.Image):
        """A wrapper class around PIL Image object, for Optical Character Recognition (OCR) purposes.

        Args:
            img (PIL.Image): The PIL Image object to be processed.
        """
        self.__img = img

    def __getattr__(self, key):
        """A magic method that allows attributes of the wrapped PIL Image object to be accessed as if they were
        attributes of this OCRImage object.

        Args:
            key (str): The name of the attribute.

        Returns:
            The value of the attribute.
        """
        if key == "__img":
            raise AttributeError()
        return getattr(self.__img, key)

    @functools.cached_property
    def dhash(self, size=64) -> str:
        """The difference hash (dhash) of the image, computed using the imagehash library.

        Args:
            size (int): The size of the hash (default: 64).

        Returns:
            The dhash of the image as a string.
        """
        return imagehash.dhash(self, size).__str__()

    @functools.cached_property
    def phash(self, size=64) -> str:
        """The perceptual hash (phash) of the image, computed using the imagehash library.

        Args:
            size (int): The size of the hash (default: 64).

        Returns:
            The phash of the image as a string.
        """
        return imagehash.phash(self, size).__str__()

    @staticmethod
    async def from_url(url: str) -> "OCRImage":
        """Create an OCRImage object from an image URL.

        Args:
            url (str): The URL of the image.

        Returns:
            OCRImage: The OCRImage object created from the image, or None if the image could not be downloaded or opened.
        """
        async with aiohttp.ClientSession() as session:
            resp = await session.post(url)
            if resp.status != 200:
                return None

            return OCRImage(Image.open(io.BytesIO(await resp.read()), mode="r").convert("L").filter(ImageFilter.SHARPEN))

    async def get_text(self) -> str:
        """Extract text from the image using OCR.

        Returns:
            str: The text extracted from the image.
        """
        if t := cache.get(self.dhash):
            return t

        return await self.run_ocr()

    @to_async()
    def run_ocr(self) -> str:
        """A helper method to run OCR on the image asynchronously.

        Returns:
            str: The text extracted from the image.
        """

        _imges = self.get_image_slices()

        _imges.append(self)
        t = ""

        for _ in _imges:
            # Resize and sharpen the image before running OCR on it

            w, h = _.size
            _ = _.resize((w * 3, h * 3)).filter(ImageFilter.SHARPEN)

            try:
                # Run OCR on the image using pytesseract library
                t += pytesseract.image_to_string(_, lang="eng", config="--oem 3 --psm 12")
            except pytesseract.TesseractError:
                continue

        cache[self.dhash] = t
        return t

    def get_image_slices(self, height: int = 400) -> List[Image.Image]:
        """
        Slices the OCRImage object into smaller images of height 'height' for more efficient OCR processing.

        Args:
            height (int): The height of each sliced image (default: 400).

        Returns:
            list: A list of PIL Image objects, each representing a sliced image.
        """

        _l = []
        imgwidth, imgheight = self.size

        # Iterate over the height of the image and slice it horizontally
        for i in range(imgheight // height):
            for j in range(imgwidth // imgwidth):
                # Calculate the bounding box for the current slice
                box = (j * imgwidth, i * height, (j + 1) * imgwidth, (i + 1) * height)
                # Crop the slice using the bounding box and append it to the list
                _l.append(self.crop(box))

        return _l
