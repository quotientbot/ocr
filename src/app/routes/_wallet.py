from __future__ import annotations


from fastapi import APIRouter

router = APIRouter()


@router.get("/user", status_code=200)
async def get_user():
    return {"balance": "100"}


@router.put("/transaction", status_code=200)
async def put_transaction():
    ...
