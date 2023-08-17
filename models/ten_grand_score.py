from .base import Base
from sqlalchemy import Column, BigInteger, String, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.enums import TenGrandCategoryArray

class TenGrandScore(Base):
    __tablename__ = "ten_grand_scores"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    created_at: Mapped[str] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[str] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    Dice: Mapped[str] = mapped_column(String(20))
    Score: Mapped[int] = mapped_column(Integer)
    Category: Mapped[str] = mapped_column(Integer)
    ten_grand_turn_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("ten_grand_turns.id"))

    def as_dict(self):
        d = {}
        for c in self.__table__.columns:
            if c.name == "Category":
                d[c.name] = TenGrandCategoryArray[getattr(self,c.name)]
            else:
                d[c.name] = getattr(self,c.name)
        return d
