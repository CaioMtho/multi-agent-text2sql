from fastapi import APIRouter, status, HTTPException
from src.vault.lib.models import NewUser, LoginRequest
from src.vault.lib.user_tools import create_user, login_user

router = APIRouter()

@router.post("/register/", status_code=status.HTTP_201_CREATED)
async def register(new_user : NewUser):
    try:
        return await create_user(new_user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)

@router.post("/login/")
async def login(request : LoginRequest):
    try:
        return await login_user(request.email, request.password)
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)
