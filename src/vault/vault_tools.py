import aiosqlite
import os
from src.vault.models import NewUser, NewSecret, Secret
from src.vault.utils import derive_key_from_password
from fernet import Fernet
from typing import Optional
import bcrypt
from contextlib import asynccontextmanager

CONNECTION_STRING="./db/vault.db"

@asynccontextmanager
async def get_conn():
    async with aiosqlite.connect(CONNECTION_STRING) as db:
        db.row_factory = aiosqlite.Row
        yield db

async def create_user(new_user : NewUser):
    salt = os.urandom(16)
    user_key_bytes = derive_key_from_password(new_user.password, salt)
    f_user = Fernet(user_key_bytes)

    master_key = Fernet.generate_key()
    wrapped_master_key = f_user.encrypt(master_key)
    password_hash = bcrypt.hashpw(new_user.password.encode('utf-8'), bcrypt.gensalt())


    async with get_conn() as db:
        try:
            stmt = "INSERT INTO users(email, password_hash, kdf_salt, wrapped_master_key) VALUES (?, ?, ?, ?)"
            await db.execute(stmt, (new_user.email, password_hash, salt, wrapped_master_key))
            await db.commit()
            return master_key
        except Exception as e:
            print(f"Erro: {e}")
            raise e
    
async def create_secret(master_key : bytes, new_secret : NewSecret):
    async with get_conn() as db:
        try:
            f_master = Fernet(master_key)
            token = f_master.encrypt(new_secret.plain_text)

            stmt = "INSERT INTO secrets (name, vault_id, ciphertext) VALUES (?, ?, ?)"
            await db.execute(stmt, (new_secret.name, new_secret.vault_id, token))
            await db.commit()

            return token
        except Exception as e:
            print(f"Erro: {e}")
            raise e
        
async def login_user(email : str, password : str):
    async with get_conn() as db:
            cursor = await db.execute("SELECT password_hash, kdf_salt, wrapped_master_key FROM users WHERE email = ?", (email,))
            result = await cursor.fetchone()
            
            if not result:
                print("Usuário não encontrado.")
                return None

            stored_hash = result['password_hash']
            if not bcrypt.checkpw(password.encode('utf-8'), stored_hash):
                print("Erro ao autenticar")
                return None

            try:
                salt = result['kdf_salt']
                wrapped_master_key = result['wrapped_master_key']

                user_key = derive_key_from_password(password, salt)
                f_user = Fernet(user_key)
                
                master_key = f_user.decrypt(wrapped_master_key)
                return master_key
                
            except Exception as e:
                print(f"Erro de criptografia (dados corrompidos?): {e}")
                raise e
        
async def get_secret(id : Optional[int], name: Optional[str], master_key : bytes) -> Secret:
    async with get_conn() as db:
            row = None
            if id is not None:
                cursor = await db.execute("SELECT * FROM secrets WHERE id = ?", (id,))
                row = await cursor.fetchone()
            elif name is not None:
                cursor = await db.execute("SELECT * FROM secrets WHERE name = ?", (name,))
                row = await cursor.fetchone()
            
            if row is None:
                return None
            
            try:
                f_master = Fernet(master_key)
                secret_bytes = f_master.decrypt(row['ciphertext'])
                plain_text = secret_bytes.decode('utf-8')

                return Secret(
                    id=row['id'],
                    vault_id=row['vault_id'],
                    name=row['name'],
                    plain_text=plain_text,
                    created_at=row['created_at']
                )
            except Exception as e:
                print(f"Erro ao desencriptar: {e}")
                raise e

                
            