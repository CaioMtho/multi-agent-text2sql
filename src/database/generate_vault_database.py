import sqlite3

with open("./scripts/03_ddl_vault.sql", "r", encoding="utf-8") as f:
    ddl = f.read()

with sqlite3.connect("./db/vault.db") as conn:
    conn.executescript(ddl)
    conn.commit()

print("DDL executado com sucesso")


