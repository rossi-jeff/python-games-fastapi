from .base import Base
from sqlalchemy import Column, BigInteger, String, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.user import User
from models.word import Word
from typing import Optional
from models.enums import GameStatusArray
from typing import List
from models.guess_word_guess import GuessWordGuess

class GuessWord(Base):
    __tablename__ = "guess_words"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    created_at: Mapped[str] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[str] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    Score: Mapped[int] = mapped_column(Integer)
    Status: Mapped[str] = mapped_column(Integer)
    user_id: Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey("users.id"), nullable=True)
    word_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("words.id"))

    user: Mapped[Optional["User"]] = relationship("User")
    word: Mapped["Word"] = relationship("Word")
    guesses: Mapped[List["GuessWordGuess"]] = relationship()
    
    def as_dict(self, includeAll: bool = False):
        d = {}
        for c in self.__table__.columns:
            if c.name == "Status":
                d[c.name] = GameStatusArray[getattr(self,c.name)]
            else:
                d[c.name] = getattr(self,c.name)
        d["user"] = getattr(self,"user")
        d["word"] = getattr(self,"word")
        if includeAll:
            d["guesses"] = []
            for guess in self.guesses:
                d["guesses"].append(guess.as_dict())
        return d