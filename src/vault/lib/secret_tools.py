from src.vault.lib.models import NewSecret, Secret
from fernet import Fernet
from typing import Optional
from src.vault.lib.connection import get_conn
    
async def create_secret(new_secret : NewSecret):
    async with get_conn() as db:
        try:
            f_master = Fernet(new_secret.master_key)
            token = f_master.encrypt(new_secret.text)

            stmt = "INSERT INTO secrets (name, vault_id, ciphertext) VALUES (?, ?, ?)"
            await db.execute(stmt, (new_secret.name, new_secret.vault_id, token))
            await db.commit()

            return token
        except Exception as e:
            print(f"Erro: {e}")
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
                    ciphertext=row['ciphertext'],
                    updated_at=row['updated_at'],
                    created_at=row['created_at']
                )
            except Exception as e:
                print(f"Erro ao desencriptar: {e}")
                raise e

                
            