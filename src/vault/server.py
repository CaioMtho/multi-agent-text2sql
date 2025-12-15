from fastapi import FastAPI, status, HTTPException
from src.vault.vault_tools import create_secret, create_user, get_secret, login_user
from src.vault.models import NewSecret, NewUser, Secret, LoginRequest
from typing import Optional

app = FastAPI(title="Vault Server")

@app.post("/register/", status_code=status.HTTP_201_CREATED)
async def register(new_user : NewUser):
    try:
        return await create_user(new_user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)
    

@app.post("/secret/", status_code=status.HTTP_201_CREATED)
async def create_secret(new_secret : NewSecret):
    try:
        return await create_secret(new_secret)
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)
    

@app.get("/secret/")
async def get_secret(id : Optional[int], name : Optional[str]):
    if not id and not name:
        raise HTTPException(status_code=400, detail="name or id needs to be not null")

    secret = await get_secret(id, name)

    return secret 

@app.post("/login/")
async def login(request : LoginRequest):
    try:
        return await login_user(request.email, request.password)
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)