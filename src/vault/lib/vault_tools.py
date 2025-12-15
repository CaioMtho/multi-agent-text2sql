from src.vault.lib.connection import get_conn
from src.vault.lib.models import NewVault, Vault
from typing import Optional

async def get_vault(name : Optional[str], id : Optional[int]) -> Vault:
    async with get_conn() as db:
        row = None
        if id is not None:
            cursor = await db.execute("SELECT * FROM vaults WHERE id = ?", (id,))
            row = await cursor.fetchone()
        elif name is not None:
            cursor = await db.execute("SELECT * FROM vaults WHERE name = ?", (name,))
            row = await cursor.fetchone()
        
        if row is None:
            return None
        
        return Vault(
            id = row['id'],
            owner_id=row['owner_id'],
            name=row['name'],
            description=row['description'],
            created_at=row['created_at'],
            updated_at=row['updated_at']
        )
    
async def get_vaults_by_owner(owner_id : int):
    async with get_conn() as db:
        if owner_id is None:
            raise ValueError("owner_id can't be None")
        
        cursor = await db.execute("SELECT * FROM vaults WHERE owner_id = ?", (owner_id,))
        rows = await cursor.fetchall()

        vaults = []

        for row in rows:
            vaults.append(Vault(
                id=row['id'],
                owner_id=row['owner_id'],
                name=row['name'],
                description=row['description'],
                created_at=row['created_at'],
                updated_at=row['updated_at']
            ))

        return vaults
    
async def create_vault(new_vault : NewVault):
    async with get_conn() as db:
        cursor = await db.execute("SELECT id FROM users WHERE id = ?", (new_vault.owner_id,))
        row = await cursor.fetchone()

        if row is None:
            raise ValueError("owner not found")
        
        await db.execute("INSERT INTO vaults(owner_id, name, description) VALUES(?, ?, ?)", (
                new_vault.owner_id, 
                new_vault.name, 
                new_vault.description
            )
        )
        
        await db.commit()

async def delete_vault(id : int):
    async with get_conn() as db:
        cursor = db.execute("DELETE FROM vaults WHERE id=?", (id,))
        
        if cursor.rowcount < 0:
                    raise ValueError("Delete does not affected any row")

        db.commit()

        
