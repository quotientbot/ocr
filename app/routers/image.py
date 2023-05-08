from fastapi import APIRouter
from typing import List

from ..consts import SS, ImageResponse

from ..utils import OCRImage

router = APIRouter()


@router.post("/ocr", status_code=200, response_model=List[ImageResponse])
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
