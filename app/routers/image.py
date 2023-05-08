from fastapi import APIRouter
from typing import List

from ..consts import Screenshot, ImageResponse

from ..utils import OCRImage


router = APIRouter()


@router.post("/ocr", status_code=200, response_model=List[ImageResponse])
async def read_items(screenshots: List[Screenshot]):

    result: List[ImageResponse] = []

    for _ in screenshots:
        _image = await OCRImage.from_url(_.url)
        if not _image:
            continue

        result.append(
            ImageResponse(
                url=_.url,
                dhash=_image.dhash,
                phash=_image.phash,
                text=await _image.get_text(),
            )
        )

    return result
