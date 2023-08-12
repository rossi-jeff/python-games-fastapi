from .base import Base
from sqlalchemy import Column, BigInteger, String, Integer, DateTime
from sqlalchemy.sql import func

class FreeCell(Base):
    __tablename__ = "free_cells"

    id = Column(BigInteger, primary_key=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    Moves = Column(Integer)
    Elapsed = Column(Integer)
    Status = Column(Integer)
    user_id = Column(BigInteger, nullable=True)
