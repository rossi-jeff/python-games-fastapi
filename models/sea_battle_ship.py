from .base import Base
from sqlalchemy import Column, BigInteger, String, Integer, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.enums import ShipTypeArray, NavyArray
from typing import List
from .sea_battle_ship_hit import SeabattleShipHit
from .sea_battle_ship_grid_point import SeaBattleShipGridPoint

class SeaBattleShip(Base):
    __tablename__ = "sea_battle_ships"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    created_at: Mapped[str] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[str] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    Type: Mapped[str] = mapped_column(Integer)
    Navy: Mapped[str] = mapped_column(Integer)
    Size: Mapped[int] = mapped_column(Integer)
    Sunk: Mapped[bool] = mapped_column(Boolean)
    sea_battle_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("sea_battles.id"))
    
    hits: Mapped[List["SeabattleShipHit"]] = relationship()
    points: Mapped[List["SeaBattleShipGridPoint"]] = relationship()
    
    def as_dict(self):
        d = {}
        for c in self.__table__.columns:
            if c.name == "Navy":
                d[c.name] = NavyArray[getattr(self,c.name)]
            elif c.name == "Type":
                d[c.name] = ShipTypeArray[getattr(self,c.name)]
            else:
                d[c.name] = getattr(self,c.name)
        d["hits"] = self.hits
        d["points"] = self.points
        return d