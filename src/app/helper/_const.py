from __future__ import annotations

from pydantic import BaseModel, HttpUrl


class SS(BaseModel):
    url: HttpUrl


class ImageResponse(BaseModel):
    url: HttpUrl
    dhash: str
    phash: str
    text: str
