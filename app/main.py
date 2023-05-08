from fastapi import FastAPI, Depends
from .routers import image

from .dependencies import verify_key

import os

os.environ["OMP_THREAD_LIMIT"] = "1"  # set limit to OpenMP threads

app = FastAPI(dependencies=[Depends(verify_key)])
app.include_router(image.router)


@app.get("/")
async def root():
    return {"ping": "pong"}
