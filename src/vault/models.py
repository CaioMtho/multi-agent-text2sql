from pydantic import BaseModel
from typing import Optional

class NewUser(BaseModel):
    username : str
    email : str
    password : str
    kdf_salt : Optional[str]
    master_key : Optional[str]
    
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