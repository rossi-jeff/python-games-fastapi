from .base import Base
from sqlalchemy import Column, BigInteger, String, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.user import User
from typing import Optional, List
from .yacht_turn import YachtTurn

class Yacht(Base):
    __tablename__ = "yachts"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    created_at: Mapped[str] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[str] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    Total: Mapped[int] = mapped_column(Integer)
    NumTurns: Mapped[int] = mapped_column(Integer)
    user_id: Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey("users.id"), nullable=True)

    user: Mapped[Optional["User"]] = relationship("User")
    turns: Mapped[List["YachtTurn"]] = relationship()
    
    def as_dict(self, includeAll: bool = False):
        d = {}
        for c in self.__table__.columns:
            d[c.name] = getattr(self,c.name)
        d["user"] = getattr(self,"user")
        if includeAll:
            d["turns"] = []
            for turn in self.turns:
                d["turns"].append(turn.as_dict())
        return d
  