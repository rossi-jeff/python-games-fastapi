from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from sqlalchemy.orm import Session
from models.hang_man import HangMan
from payloads.hang_man_payload import HangManCreate, HangManGuess
from utilities.guess_word import ListContains

router = APIRouter(
    prefix="/api/hang_man",
    tags=["Hang Man"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def hang_men_paginated(Limit: int = 10, Offset: int = 0, db: Session = Depends(get_db)):
    count = db.query(HangMan).where(HangMan.Status != 1).count()
    items = []
    hang_men = db.query(HangMan).where(HangMan.Status != 1).order_by(
        HangMan.Status.desc(),
        HangMan.Score.desc()
    ).limit(Limit).offset(Offset).all()
    for hm in hang_men:
        items.append(hm.as_dict())
    return {"Count": count, "Limit": Limit, "Offset": Offset, "Items": items}

@router.get("/{hang_man_id}")
async def get_hang_man_by_id(hang_man_id: int, db: Session = Depends(get_db)):
    hang_man = db.query(HangMan).where(HangMan.id == hang_man_id).first()
    if hang_man is None:
        raise HTTPException(status_code=404, detail="Hang Man not found")
    return hang_man.as_dict()

@router.post("/")
async def create_hang_man(body: HangManCreate, db: Session = Depends(get_db)):
    hang_man = HangMan(
        word_id = body.WordId,
        Status = 1,
        Score = 0,
        Correct = "",
        Wrong = ""
    )
    db.add(hang_man)
    db.commit()
    db.refresh(hang_man)
    return hang_man.as_dict()

@router.post("/{hang_man_id}/guess")
async def hang_man_guess(hang_man_id: int, body: HangManGuess, db: Session = Depends(get_db)):
    hang_man = db.query(HangMan).where(HangMan.id == hang_man_id).first()
    if hang_man is None:
        raise HTTPException(status_code=404, detail="Hang Man not found")
    correct = list(hang_man.Correct)
    wrong = list(hang_man.Wrong)
    word = list(body.Word)
    found: bool = ListContains(body.Letter,word)
    if found:
        correct.append(body.Letter)
    else:
        wrong.append(body.Letter)
    hang_man.Correct = ",".join(correct)
    hang_man.Wrong = ",".join(wrong)
    db.add(hang_man)
    db.commit()
    db.refresh(hang_man)
    return { "Letter": body.Letter, "Found": found }