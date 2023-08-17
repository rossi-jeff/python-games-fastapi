from .base import Base
from sqlalchemy import Column, BigInteger, String, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from .ten_grand_score import TenGrandScore

class TenGrandTurn(Base):
    __tablename__ = "ten_grand_turns"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    created_at: Mapped[str] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[str] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    Score: Mapped[int] = mapped_column(Integer)
    ten_grand_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("ten_grands.id"))

    scores: Mapped[List["TenGrandScore"]] = relationship()

    def as_dict(self):
        d = {}
        for c in self.__table__.columns:
            d[c.name] = getattr(self,c.name)
        d["scores"] = []
        for score in self.scores:
            d["scores"].append(score.as_dict())
        return d