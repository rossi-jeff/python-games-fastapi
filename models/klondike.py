from .base import Base
from sqlalchemy import Column, BigInteger, String, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.user import User
from typing import Optional
from models.enums import GameStatusArray

class Klondike(Base):
    __tablename__ = "klondikes"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    created_at: Mapped[str] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[str] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    Moves: Mapped[int] = mapped_column(Integer)
    Elapsed: Mapped[int] = mapped_column(Integer)
    Status: Mapped[str] = mapped_column(Integer)
    user_id: Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey("users.id"), nullable=True)

    user: Mapped[Optional["User"]] = relationship("User")

    def as_dict(self):
        d = {}
        for c in self.__table__.columns:
            if c.name == "Status":
                d[c.name] = GameStatusArray[getattr(self,c.name)]
            else:
                d[c.name] = getattr(self,c.name)
        d["user"] = getattr(self,"user")
        return d