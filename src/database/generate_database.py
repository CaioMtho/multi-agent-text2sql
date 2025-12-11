import duckdb

conn = duckdb.connect("./db/main.duckdb")

with open("./scripts/01_ddl.sql", "r") as f:
    ddl = f.read()

conn.execute(ddl)
print("DDL executado com sucesso")

with open("./scripts/02_data.sql", "r") as f:
    sql = f.read()

conn.execute(sql)

print("Data executado com sucesso")

conn.commit()

data = conn.execute("SELECT * FROM clientes")
print(data.fetchall())
conn.close()

