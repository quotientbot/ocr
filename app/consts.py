from pydantic import BaseModel, HttpUrl


class Screenshot(BaseModel):
    url: HttpUrl


class ImageResponse(BaseModel):
    url: HttpUrl
    dhash: str
    phash: str
    text: str
