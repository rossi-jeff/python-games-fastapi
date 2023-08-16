from .base import Base
from sqlalchemy import Column, BigInteger, String, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

class TenGrandScore():
    __tablename__ = "ten_grand_scores"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    created_at: Mapped[str] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[str] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    Dice: Mapped[str] = mapped_column(String(20))
    Score: Mapped[int] = mapped_column(Integer)
    Category: Mapped[str] = mapped_column(Integer)
    ten_grand_turn_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("ten_grand_turns.id"))