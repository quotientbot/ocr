from __future__ import annotations

import os

from decouple import config
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import APIKeyHeader

from .routes._image import router as _image_router

api_scheme = APIKeyHeader(name="authorization")
os.environ["OMP_THREAD_LIMIT"] = "1"


async def verify_key(key: str = Depends(api_scheme)) -> None:
    if key != config("FASTAPI_KEY"):
        raise HTTPException(status_code=403)


app = FastAPI(dependencies=[Depends(verify_key)])


@app.get("/")
async def root() -> dict:
    return {"ping": "pong"}


app.include_router(_image_router)
