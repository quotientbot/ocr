from __future__ import annotations

from typing import List

from fastapi import APIRouter

from utils import OCRImage

from ..helper._const import SS, ImageResponse

router = APIRouter()


@router.post("/ocr", status_code=200, response_model=List[ImageResponse])
async def read_items(screen_shots: List[SS]) -> List[ImageResponse]:
    data: List[ImageResponse] = []

    for screen_shot in screen_shots:
        image = await OCRImage.from_url(screen_shot.url)
        if image:
            data.append(
                ImageResponse(
                    url=screen_shot.url,
                    dhash=image.dhash,
                    phash=image.phash,
                    text=await image.get_text(),
                )
            )

    return data
