from .base import Base
from sqlalchemy import Column, BigInteger, String, Integer, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    created_at: Mapped[str] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[str] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    UserName: Mapped[str] = mapped_column(String(30))
    password_digest: Mapped[str] = mapped_column(String(255))
    