from .base import Base
from sqlalchemy import Column, BigInteger, String, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

class SeaBattleShipGridPoint(Base):
    __tablename__ = "sea_battle_ship_grid_points"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    created_at: Mapped[str] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[str] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    Horizontal: Mapped[str] = mapped_column(String(1))
    Vertical: Mapped[int] = mapped_column(Integer)
    sea_battle_ship_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("sea_battle_ships.id"))