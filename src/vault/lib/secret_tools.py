from src.vault.lib.models import NewSecret, Secret
from fernet import Fernet
from typing import Optional
from src.vault.lib.connection import get_conn
    
async def create_secret(new_secret : NewSecret):
    async with get_conn() as db:
        f_master = Fernet(new_secret.master_key)
        token = f_master.encrypt(new_secret.text)

        stmt = "INSERT INTO secrets (name, vault_id, ciphertext) VALUES (?, ?, ?)"
        cursor = await db.execute(stmt, (new_secret.name, new_secret.vault_id, token))
        await db.commit()

        row = cursor.lastrowid

        return Secret(
            id = row['id'],
            vault_id = row['vault_id'],
            name=row['name'],
            ciphertext=row['ciphertext'],
            created_at=row['created_at'],
            updated_at=row['updated_at']
        )

async def get_secret_by_id(id : int, master_key : bytes) -> Secret:
    async with get_conn() as db:
        cursor = await db.execute("SELECT * FROM secrets WHERE id = ?", (id,))
        row = await cursor.fetchone()
        
        if row is None:
            return None
        
        f_master = Fernet(master_key)
        secret_bytes = f_master.decrypt(row['ciphertext'])
        plain_text = secret_bytes.decode('utf-8')

        return Secret(
            id=row['id'],
            vault_id=row['vault_id'],
            name=row['name'],
            plain_text=plain_text,
            ciphertext=row['ciphertext'],
            updated_at=row['updated_at'],
            created_at=row['created_at']
        )

async def get_secrets(vault_id : int,  master_key : bytes, name : Optional[str] = None):
    async with get_conn() as db:
        if name is not None:
            cursor = await db.execute("SELECT * FROM secrets WHERE vault_id = ? AND name LIKE '%?%'", (vault_id, name))
        else:
            cursor = await db.execute("SELECT * FROM secrets WHERE vault_id = ?", (vault_id,))

        result = await cursor.fetchall()

        secrets = []

        f_master = Fernet(master_key)

        for row in result:
            secret_bytes = f_master.decrypt(row['ciphertext'])
            plain_text = secret_bytes.decode('utf-8')

            secrets.append(Secret(
            id=row['id'],
            vault_id=row['vault_id'],
            name=row['name'],
            plain_text=plain_text,
            ciphertext=row['ciphertext'],
            updated_at=row['updated_at'],
            created_at=row['created_at']
        ))
            
async def delete_secret(id : int, master_key : bytes):
    async with get_conn() as db:
        cursor = await db.execute("SELECT ciphertext FROM secrets WHERE id=?", (id))
        ciphertext = cursor.fetchone['ciphertext']
        f_master = Fernet(master_key)
        f_master.decrypt(ciphertext)

        cursor = await db.execute("DELETE FROM secrets WHERE id=?", (id,))

        await db.commit()


