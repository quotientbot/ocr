from __future__ import annotations

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import APIKeyHeader
from os import environ

# from .routes._bot import router as _bot_router
# I have no Idea regarding the DATABASE
from .routes._image import router as _image_router

api_scheme = APIKeyHeader(name="authorization")


async def verify_key(key: str = Depends(api_scheme)):
    if key != environ.get("FASTAPI_KEY"):
        raise HTTPException(status_code=403)


app = FastAPI(dependencies=[Depends(verify_key)])


@app.get("/")
async def root():
    return {"ping": "pong"}


# app.include_router(_bot_router)
app.include_router(_image_router)
