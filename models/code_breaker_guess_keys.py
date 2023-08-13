from .base import Base
from sqlalchemy import Column, BigInteger, String, DateTime, ForeignKey, Integer
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.enums import KeysArray

class CodeBreakerGuessKey(Base):
    __tablename__ = "code_breaker_guess_keys"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    created_at: Mapped[str] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[str] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    code_breaker_guess_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("code_breaker_guesses.id"))
    Key: Mapped[int] = mapped_column(Integer)

    def as_dict(self):
        d = {}
        for c in self.__table__.columns:
            if c.name == "Key":
                d[c.name] = KeysArray[getattr(self,c.name)]
            else:
                d[c.name] = getattr(self,c.name)
        return d