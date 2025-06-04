import sys
from pathlib import Path

from fastapi import FastAPI, Request, Response

from app.db.postgres import AsyncSessionLocal
from app.api.routers import wallet, balance

sys.path.append(str(Path(__file__).parent))

app = FastAPI()

app.include_router(wallet.router)
app.include_router(balance.router)