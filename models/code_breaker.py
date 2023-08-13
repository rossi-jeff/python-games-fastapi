from .base import Base
from sqlalchemy import Column, BigInteger, String, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.user import User
from typing import Optional
from models.enums import GameStatusArray
from typing import List
from models.code_breaker_guess import CodeBreakerGuess
from models.code_breaker_code import CodeBreakerCode

class CodeBreaker(Base):
    __tablename__ = "code_breakers"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    created_at: Mapped[str] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[str] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    Columns: Mapped[int] = mapped_column(Integer)
    Colors: Mapped[int] = mapped_column(Integer)
    Score: Mapped[int] = mapped_column(Integer)
    Available: Mapped[str] = mapped_column(String(75))
    Status: Mapped[str] = mapped_column(Integer)
    user_id: Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey("users.id"), nullable=True)

    user: Mapped[Optional["User"]] = relationship("User")
    guesses: Mapped[List["CodeBreakerGuess"]] = relationship()
    codes: Mapped[List["CodeBreakerCode"]] = relationship()

    def as_dict(self, includeAll: bool = False):
        d = {}
        for c in self.__table__.columns:
            if c.name == "Status":
                d[c.name] = GameStatusArray[getattr(self,c.name)]
            else:
                d[c.name] = getattr(self,c.name)
        d["user"] = getattr(self,"user")
        if includeAll:
            d["codes"] = []
            for code in self.codes:
                d["codes"].append(code.as_dict())
            d["guesses"] = []
            for guess in self.guesses:
                d["guesses"].append(guess.as_dict())
        return d
