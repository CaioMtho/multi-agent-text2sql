from src.vault.lib.connection import get_conn
from fernet import Fernet
from src.vault.lib.utils import derive_key_from_password
from src.vault.lib.models import NewUser
import os
import bcrypt

async def login_user(email : str, password : str):
    async with get_conn() as db:
        cursor = await db.execute("SELECT id, password_hash, kdf_salt, wrapped_master_key FROM users WHERE email = ?", (email,))
        result = await cursor.fetchone()
        
        if not result:
            print("Usuário não encontrado.")
            return None

        stored_hash = result['password_hash']
        if not bcrypt.checkpw(password.encode('utf-8'), stored_hash):
            print("Erro ao autenticar")
            return None

        salt = result['kdf_salt']
        wrapped_master_key = result['wrapped_master_key']

        user_key = derive_key_from_password(password, salt)
        f_user = Fernet(user_key)
        
        master_key = f_user.decrypt(wrapped_master_key)
        return {result['id'], master_key}

async def create_user(new_user : NewUser):
    salt = os.urandom(16)
    user_key_bytes = derive_key_from_password(new_user.password, salt)
    f_user = Fernet(user_key_bytes)

    master_key = Fernet.generate_key()
    wrapped_master_key = f_user.encrypt(master_key)
    password_hash = bcrypt.hashpw(new_user.password.encode('utf-8'), bcrypt.gensalt())

    async with get_conn() as db:
        stmt = "INSERT INTO users(email, password_hash, kdf_salt, wrapped_master_key) VALUES (?, ?, ?, ?)"
        await db.execute(stmt, (new_user.email, password_hash, salt, wrapped_master_key))
        await db.commit()
        return master_key