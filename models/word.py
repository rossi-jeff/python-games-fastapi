from .base import Base
from sqlalchemy import Column, BigInteger, String, Integer, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column

class Word(Base):
    __tablename__ = "words"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    created_at: Mapped[str] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[str] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    Word: Mapped[str] = mapped_column(String(30))
    Length: Mapped[int] = mapped_column(Integer)