from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.services import CreateWalletHash
from app.repositories import WalletManager, get_db

def get_wallet_hash():
    return CreateWalletHash()

def get_wallet_manager(session: AsyncSession = Depends(get_db)):
    return WalletManager(session)