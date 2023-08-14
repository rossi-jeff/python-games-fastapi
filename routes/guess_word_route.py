from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from models.guess_word import GuessWord
from sqlalchemy.orm import Session, joinedload

router = APIRouter(
    prefix="/api/guess_word",
    tags=["Guess Word"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def guess_words_paginated(Limit: int = 10, Offset: int = 0, db: Session = Depends(get_db)):
    count = db.query(GuessWord).where(GuessWord.Status != 1).count()
    items = []
    guess_words = db.query(GuessWord).where(GuessWord.Status != 1).order_by(
        GuessWord.Status.desc(),
        GuessWord.Score.desc()
		).limit(Limit).offset(Offset).all()
    for gw in guess_words:
        items.append(gw.as_dict())
    return {"Count": count, "Limit": Limit, "Offset": Offset, "Items": items}

@router.get("/{guess_word_id}")
async def get_guess_word_by_id(guess_word_id: int, db: Session = Depends(get_db)):
    guess_word = db.query(GuessWord).where(GuessWord.id == guess_word_id).first()
    if guess_word is None:
        raise HTTPException(status_code=404, detail="Guess Word not found")
    return guess_word.as_dict(True)