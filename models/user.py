from .base import Base
from sqlalchemy import Column, BigInteger, String, Integer, DateTime

class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    UserName = Column(String(30))
    password_digest = Column(String(255))
    