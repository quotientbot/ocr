from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader
from decouple import config

api_scheme = APIKeyHeader(name="authorization")


async def verify_key(key: str = Depends(api_scheme)):
    if key not in [config("FASTAPI_KEY"), config("TEMP_KEY")]:
        raise HTTPException(status_code=403, detail="Invalid API key")
