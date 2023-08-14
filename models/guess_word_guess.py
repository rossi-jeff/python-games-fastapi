from .base import Base
from sqlalchemy import Column, BigInteger, String, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from models.guess_word_guess_rating import GuessWordGuessRating


class GuessWordGuess(Base):
    __tablename__ = "guess_word_guesses"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    created_at: Mapped[str] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[str] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    guess_word_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("guess_words.id"))
    Guess: Mapped[str] = mapped_column(String(30))
    
    ratings: Mapped[List["GuessWordGuessRating"]] = relationship()
    
    def as_dict(self):
        d = {}
        for c in self.__table__.columns:
            d[c.name] = getattr(self,c.name)
        d["ratings"] = []
        for rating in self.ratings:
            d["ratings"].append(rating.as_dict())
        return d
  