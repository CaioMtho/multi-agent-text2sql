from pydantic import BaseModel
from typing import Optional

class LoginRequest(BaseModel):
    email : str
    password: str

class NewUser(BaseModel):
    email : str
    password : str
    kdf_salt : Optional[str] = None
    master_key : Optional[str] = None
    
class User(BaseModel):
    id : int
    email : str
    kdf_salt : str

class NewSecret(BaseModel):
    vault_id : int
    name : str
    text : str
    master_key : bytes

class Secret(BaseModel):
    id : int
    vault_id: int
    name : str
    ciphertext: str
    plain_text : Optional[str] = None
    created_at : str
    updated_at : str

class NewVault(BaseModel):
    owner_id : int
    name : str
    description : Optional[str] = None

class Vault(BaseModel):
    id : int
    owner_id : int
    name : str
    description : Optional[str]
    created_at : str
    updated_at : str