from __future__ import annotations

from fastapi import APIRouter, status
from typing import List

from ..helper._const import SS, ImageResponse

# I don't know in my IDE the imports were broken without `src.`
# even tho' they are in same directory...
from ..helper.image import get_image, get_image_dhash, get_image_phash, get_image_string
from utils import OCRImage

router = APIRouter()


@router.post("/ocr", status_code=status.HTTP_200_OK, response_model=List[ImageResponse])
async def read_items(_shots: List[SS]):

    _result: List[ImageResponse] = []

    for _ in _shots:
        _image = await get_image(_)
        if not _image:
            continue

        _result.append(
            ImageResponse(
                url=_.url,
                dhash=str(await get_image_dhash(_image)),
                phash=str(await get_image_phash(_image)),
                text=await get_image_string(_image),
            )
        )

    return _result


@router.post("/rocr", status_code=200, response_model=List[ImageResponse])
async def read_items(_shots: List[SS]):

    _result: List[ImageResponse] = []

    for _ in _shots:
        _image = await OCRImage.from_url(_.url)
        if not _image:
            continue

        _result.append(
            ImageResponse(
                url=_.url,
                dhash=_image.dhash,
                phash=_image.phash,
                text=await _image.get_text(),
            )
        )

    return _result
