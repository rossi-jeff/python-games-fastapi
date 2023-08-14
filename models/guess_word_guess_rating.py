from .base import Base
from sqlalchemy import Column, BigInteger, String, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.enums import RatingArray

class GuessWordGuessRating(Base):
    __tablename__ = "guess_word_guess_ratings"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    created_at: Mapped[str] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[str] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    guess_word_guess_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("guess_word_guesses.id"))
    Rating: Mapped[str] = mapped_column(Integer)
    
    def as_dict(self):
        d = {}
        for c in self.__table__.columns:
            if c.name == "Rating":
                d[c.name] = RatingArray[getattr(self,c.name)]
            else:
                d[c.name] = getattr(self,c.name)
        return d