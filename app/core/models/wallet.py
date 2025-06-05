from sqlalchemy.orm import  mapped_column, Mapped
from sqlalchemy import Integer, String
from app.core.database import Base

class Wallet(Base):
    __tablename__ = 'wallet'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    total: Mapped[int] = mapped_column(Integer, default=0)
    wallet_id: Mapped[str] = mapped_column(String(32), unique=True)
