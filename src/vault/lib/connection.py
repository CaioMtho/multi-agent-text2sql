from contextlib import asynccontextmanager
import aiosqlite

CONNECTION_STRING="./db/vault.db"

@asynccontextmanager
async def get_conn():
    async with aiosqlite.connect(CONNECTION_STRING) as db:
        db.row_factory = aiosqlite.Row
        yield db