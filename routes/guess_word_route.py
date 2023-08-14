from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from models.guess_word import GuessWord
from models.guess_word_guess import GuessWordGuess
from sqlalchemy.orm import Session, joinedload
from models.word import Word
from payloads.guess_word_payload import GuessWordCreate, GuessWordGuessPayload, GuessWordHint
from utilities.guess_word import (
    MatchGreen,
    MatchBrown,
    MatchGray,
    IncludeAllBrown
)

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

@router.post("/")
async def create_guess_word(body: GuessWordCreate, db: Session = Depends(get_db)):
    guess_word = GuessWord(
        word_id = body.WordId,
        Score = 0,
        Status = 1
    )
    db.add(guess_word)
    db.commit()
    db.refresh(guess_word)
    return guess_word.as_dict()

@router.post("/{guess_word_id}/guess")
async def take_guess_word_guess(guess_word_id: int, body: GuessWordGuessPayload, db: Session = Depends(get_db)):
    return { "message": "TODO" }

@router.post("/hint")
async def get_guess_word_hints(body: GuessWordHint, db: Session = Depends(get_db)):
    hints = []
    words = db.query(Word).where(Word.Length == body.Length).all()
    print("words",len(words))
    for w in words:
        word = w.Word
        if (MatchGreen(word,body.Green) 
                and not MatchGray(word,body.Gray,body.Green) 
                and not MatchBrown(word,body.Brown) 
                and IncludeAllBrown(word,body.Brown)
                ):
            hints.append(word)
    return hints
