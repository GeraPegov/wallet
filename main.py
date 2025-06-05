# import sys
# from pathlib import Path

from fastapi import FastAPI

from app.api.router import api_router

# sys.path.append(str(Path(__file__).parent))

app = FastAPI(
    title='Wallet'
)

app.include_router(api_router)
