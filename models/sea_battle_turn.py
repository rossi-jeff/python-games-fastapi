from .base import Base
from sqlalchemy import Column, BigInteger, String, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from models.enums import ShipTypeArray, NavyArray, TargetArray

class SeaBattleTurn(Base):
    __tablename__ = "sea_battle_turns"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    created_at: Mapped[str] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[str] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    ShipType: Mapped[Optional[str]] = mapped_column(Integer, nullable=True)
    Navy: Mapped[str] = mapped_column(Integer)
    Target: Mapped[str] = mapped_column(Integer)
    Horizontal: Mapped[str] = mapped_column(String(1))
    Vertical: Mapped[int] = mapped_column(Integer)
    sea_battle_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("sea_battles.id"))
    
    def as_dict(self):
        d = {}
        for c in self.__table__.columns:
            if c.name == "Target":
                d[c.name] = TargetArray[getattr(self,c.name)]
            elif c.name == "Navy":
                d[c.name] = NavyArray[getattr(self,c.name)]
            elif c.name == "ShipType":
                val = getattr(self,c.name)
                if val is None:
                    d[c.name] = val
                else:
                    d[c.name] = ShipTypeArray[val]
            else:
                d[c.name] = getattr(self,c.name)
        return d