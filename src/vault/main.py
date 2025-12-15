from fastapi import FastAPI
import src.vault.routes.secrets as secrets
import src.vault.routes.users as users
import src.vault.routes.vaults as vaults

app = FastAPI(title="Vault Server")

app.include_router(secrets.router)
app.include_router(users.router)
app.include_router(vaults.router)

