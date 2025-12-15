import aiosqlite
import asyncio
from contextlib import asynccontextmanager
CONNECTION_STRING="./db/vault.db"

@asynccontextmanager
async def get_conn():
    async with aiosqlite.connect(CONNECTION_STRING) as db:
        db.row_factory = aiosqlite.Row
        yield db
    
async def test():
    async with get_conn() as conn:
        cursor = await conn.execute("SELECT 1 AS number")
        result = await cursor.fetchone()
        print(result['number'])

if __name__ == "__main__":
    asyncio.run(test())