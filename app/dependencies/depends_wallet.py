from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import WalletManager, get_db
from app.services import CreateWalletHash


def get_wallet_hash():
    return CreateWalletHash()


def get_wallet_manager(session: AsyncSession = Depends(get_db)):
    return WalletManager(session)
