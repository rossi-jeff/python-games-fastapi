from .base import Base
from sqlalchemy import Column, BigInteger, String, Integer, DateTime

class Word(Base):
    __tablename__ = "words"

    id = Column(BigInteger, primary_key=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    Word = Column(String(30)) 
    Length = Column(Integer)