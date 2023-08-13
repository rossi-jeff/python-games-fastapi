from .base import Base
from sqlalchemy import Column, BigInteger, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.code_breaker_guess_color import CodeBreakerGuessColor
from models.code_breaker_guess_keys import CodeBreakerGuessKey
from typing import List

class CodeBreakerGuess(Base):
    __tablename__ = "code_breaker_guesses"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    created_at: Mapped[str] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[str] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    code_breaker_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("code_breakers.id"))

    colors: Mapped[List["CodeBreakerGuessColor"]] = relationship()
    keys: Mapped[List["CodeBreakerGuessKey"]] = relationship()

    def as_dict(self):
        d = {}
        for c in self.__table__.columns:
            d[c.name] = getattr(self,c.name)
        d["colors"] = []
        for color in self.colors:
            d["colors"].append(color.as_dict())
        d["keys"] = []
        for key in self.keys:
            d["keys"].append(key.as_dict())
        return d