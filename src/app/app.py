from __future__ import annotations

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import APIKeyHeader
from decouple import config

from .routes._image import router as _image_router
from .routes._wallet import router as _wallet_router

from tortoise.contrib.fastapi import register_tortoise
import os

api_scheme = APIKeyHeader(name="authorization")
os.environ["OMP_THREAD_LIMIT"] = "1"


async def verify_key(key: str = Depends(api_scheme)):
    if key != config("FASTAPI_KEY"):
        raise HTTPException(status_code=403)


app = FastAPI(dependencies=[Depends(verify_key)])


@app.get("/")
async def root():
    return {"ping": "pong"}


app.include_router(_image_router)
app.include_router(_wallet_router)

# register_tortoise(
#     app,
#     db_url="sqlite://:memory:",
#     modules={"models": ["models"]},
# )
