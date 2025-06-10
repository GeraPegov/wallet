
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core import Base


class Wallet(Base):
    __tablename__ = 'wallet'
    __table_args__ = {'schema': 'public'}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    total: Mapped[int] = mapped_column(Integer, default=0)
    wallet_id: Mapped[str] = mapped_column(String(32), unique=True)


