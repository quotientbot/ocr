from __future__ import annotations

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import APIKeyHeader
from decouple import config

from .routes._image import router as _image_router

api_scheme = APIKeyHeader(name="authorization")


async def verify_key(key: str = Depends(api_scheme)):
    if key != config("FASTAPI_KEY"):
        print(key)
        print(config("FASTAPI_KEY"))
        raise HTTPException(status_code=403)


app = FastAPI(dependencies=[Depends(verify_key)])


@app.get("/")
async def root():
    return {"ping": "pong"}


app.include_router(_image_router)
