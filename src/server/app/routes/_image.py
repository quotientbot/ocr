from __future__ import annotations

from fastapi import APIRouter, status
from typing import List

from ..helper._const import SS
from src.models import ImageResponse
# I don't know in my IDE the imports were broken without `src.`
# even tho' they are in same directory...
from ..helper.image import get_image, get_image_dhash, get_image_phash, get_image_string
import asyncio

router = APIRouter()


sem: asyncio.Semaphore = asyncio.Semaphore(3)


@router.post("/ocr", status_code=status.HTTP_200_OK, response_model=List[ImageResponse])
async def read_items(_shots: List[SS]):

    _result: List[ImageResponse] = []

    async with sem:
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
