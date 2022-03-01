from pydantic import BaseModel, HttpUrl


class ImageResponse(BaseModel):
    url: HttpUrl
    dhash: str
    phash: str
    text: str

    @property
    def lower_text(self):
        return self.text.lower().replace(" ", "").replace("\n", "")