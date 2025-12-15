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
    
class NewSecret(BaseModel):
    vault_id : int
    name : str
    text : str

class Secret(BaseModel):
    id : int
    vault_id: int
    name : str
    ciphertext: str
    plain_text : Optional[str] 
    created_at : str
    updated_at : str