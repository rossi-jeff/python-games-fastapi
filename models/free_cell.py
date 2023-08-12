from .base import Base
from sqlalchemy import Column, BigInteger, String, Integer, DateTime, ForeignKey

class FreeCell(Base):
    __tablename__ = "free_cells"

    id = Column(BigInteger, primary_key=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    Moves = Column(Integer)
    Elapsed = Column(Integer)
    Status = Column(Integer)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=True)
