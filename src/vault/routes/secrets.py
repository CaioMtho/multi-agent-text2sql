from fastapi import APIRouter, status, HTTPException
from src.vault.lib.secret_tools import get_secret, create_secret
from src.vault.lib.models import NewSecret
from typing import Optional

router = APIRouter()

@router.post("/secret/", status_code=status.HTTP_201_CREATED)
async def create(new_secret : NewSecret):
    try:
        return await create_secret(new_secret)
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)
    

@router.get("/secret/")
async def get(master_key : str, id : Optional[int] = None, name : Optional[str] = None):
    if not id and not name:
        raise HTTPException(status_code=400, detail="name or id needs to be not null")

    secret = await get_secret(id, name, master_key.encode('utf-8'))

    return secret 