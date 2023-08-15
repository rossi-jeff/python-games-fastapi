from .base import Base
from sqlalchemy import Column, BigInteger, String, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.user import User
from typing import Optional
from models.enums import GameStatusArray
from typing import List
from .sea_battle_ship import SeaBattleShip
from .sea_battle_turn import SeaBattleTurn

class SeaBattle(Base):
    __tablename__ = "sea_battles"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    created_at: Mapped[str] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[str] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    Axis: Mapped[int] = mapped_column(Integer)
    Score: Mapped[int] = mapped_column(Integer)
    Status: Mapped[str] = mapped_column(Integer)
    user_id: Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey("users.id"), nullable=True)

    user: Mapped[Optional["User"]] = relationship("User")
    ships: Mapped[List["SeaBattleShip"]] = relationship()
    turns: Mapped[List["SeaBattleTurn"]] = relationship()

    def as_dict(self, includeAll: bool = False):
        d = {}
        for c in self.__table__.columns:
            if c.name == "Status":
                d[c.name] = GameStatusArray[getattr(self,c.name)]
            else:
                d[c.name] = getattr(self,c.name)
        d["user"] = getattr(self,"user")
        if includeAll:
            d["ships"] = []
            for ship in self.ships:
                d["ships"].append(ship.as_dict())
            d["turns"] = []
            for turn in self.turns:
                d["turns"].append(turn.as_dict())
        return d
  