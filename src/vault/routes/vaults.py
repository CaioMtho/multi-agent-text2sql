from fastapi import APIRouter, HTTPException
from src.vault.lib.vault_tools import get_vault, get_vaults_by_owner, create_vault
from src.vault.lib.models import NewVault
from typing import Optional
router = APIRouter()

@router.get("/vaults/")
async def get_by_id(id : Optional[int] = None, name : Optional[str] = None):
    if id is None and name is None:
        raise HTTPException(status_code=400, detail="name or id needs to be not None")
    
    return await get_vault(name, id)

@router.get("/vaults/{owner_id}")
async def get_by_owner_id(owner_id : int):
    if owner_id is None:
        raise HTTPException(status_code=400, detail="owner_id cant be none")
    
    return await get_vaults_by_owner(owner_id)

@router.post("/vaults/")
async def create(new_vault : NewVault):
    try:
        await create_vault(new_vault)
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)