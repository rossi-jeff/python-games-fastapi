from .base import Base
from sqlalchemy import Column, BigInteger, String, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

class TenGrandTurn():
    __tablename__ = "ten_grand_turns"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    created_at: Mapped[str] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[str] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    Score: Mapped[int] = mapped_column(Integer)
    ten_grand_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("ten_grands.id"))