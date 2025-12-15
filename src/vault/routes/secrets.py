from fastapi import APIRouter, status, HTTPException
from src.vault.lib.secret_tools import get_secret_by_id, create_secret, get_secrets
from src.vault.lib.models import NewSecret
from typing import Optional

router = APIRouter()

@router.post("/secret/", status_code=status.HTTP_201_CREATED)
async def create(new_secret : NewSecret):
    try:
        return await create_secret(new_secret)
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)
    

@router.get("/secret/{id}")
async def get(master_key : str, id : int):
    try:
        secret = await get_secret_by_id(id, master_key.encode('utf-8'))
        return secret
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)
    
@router.get("/secret/")
async def get()