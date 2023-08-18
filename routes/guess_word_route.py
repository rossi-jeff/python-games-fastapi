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
    IncludeAllBrown,
    CalculateGuessRatings
)
from models.guess_word_guess import GuessWordGuess
from optional_auth import get_current_user
from typing import Optional

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

@router.get("/progress")
async def guess_words_in_progress(db: Session = Depends(get_db), user_id: Optional[str] = Depends(get_current_user)):
    items = []
    if user_id is not None:
        guess_words = db.query(GuessWord).where(GuessWord.Status == 1).filter(GuessWord.user_id == user_id).all()
        for gw in guess_words:
            items.append(gw.as_dict())
    return items

@router.get("/{guess_word_id}")
async def get_guess_word_by_id(guess_word_id: int, db: Session = Depends(get_db)):
    guess_word = db.query(GuessWord).where(GuessWord.id == guess_word_id).first()
    if guess_word is None:
        raise HTTPException(status_code=404, detail="Guess Word not found")
    return guess_word.as_dict(True)

@router.post("/")
async def create_guess_word(body: GuessWordCreate, db: Session = Depends(get_db), user_id: Optional[str] = Depends(get_current_user)):
    guess_word = GuessWord(
        word_id = body.WordId,
        Score = 0,
        Status = 1
    )
    if user_id is not None:
        guess_word.user_id = user_id
    db.add(guess_word)
    db.commit()
    db.refresh(guess_word)
    return guess_word.as_dict()

@router.post("/{guess_word_id}/guess")
async def take_guess_word_guess(guess_word_id: int, body: GuessWordGuessPayload, db: Session = Depends(get_db)):
    guess_word_guess = GuessWordGuess(
        guess_word_id = guess_word_id,
        Guess = body.Guess
    )
    db.add(guess_word_guess)
    db.commit()
    db.refresh(guess_word_guess)
    CalculateGuessRatings(db,guess_word_guess.id,body.Guess,body.Word)
    db.refresh(guess_word_guess)
    return guess_word_guess.as_dict()

@router.post("/hint")
async def get_guess_word_hints(body: GuessWordHint, db: Session = Depends(get_db)):
    hints = []
    words = db.query(Word).where(Word.Length == body.Length).all()
    print("words",len(words))
    for w in words:
        word = w.Word
        if not MatchGreen(word,body.Green):
            continue
        if MatchGray(word,body.Gray,body.Green):
            continue
        if MatchBrown(word,body.Brown):
            continue
        if not IncludeAllBrown(word,body.Brown):
            continue
        hints.append(word)
    return hints
