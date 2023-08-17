from .base import Base
from sqlalchemy import Column, BigInteger, String, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from .enums import YachtCategoryArray

class YachtTurn(Base):
    __tablename__ = "yacht_turns"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    created_at: Mapped[str] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[str] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    RollOne: Mapped[Optional[str]] = mapped_column(String(20))
    RollTwo: Mapped[Optional[str]] = mapped_column(String(20))
    RollThree: Mapped[Optional[str]] = mapped_column(String(20))
    Score: Mapped[int] = mapped_column(Integer)
    Category: Mapped[Optional[str]] = mapped_column(Integer, nullable=True)
    yacht_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("yachts.id"))
    
    def as_dict(self):
        d = {}
        for c in self.__table__.columns:
            if c.name == "Category":
                val = getattr(self,c.name)
                if val is not None:
                    d[c.name] = YachtCategoryArray[val]
                else:
                    d[c.name] = val
            else:
                d[c.name] = getattr(self,c.name)
        return d
