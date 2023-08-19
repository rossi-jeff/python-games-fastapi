from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from sqlalchemy.orm import Session
from models.hang_man import HangMan
from payloads.hang_man_payload import HangManCreate, HangManGuess
from utilities.guess_word import ListContains
from utilities.hang_man import CalculateHangManStatus, CalculateHangManScore, StringListUnique
from models.enums import GameStatusArray
from optional_auth import get_current_user
from typing import Optional, List
from responses.hang_man_response import HangManResponse, HangManPaginatedResponse, HangManGuessResponse

router = APIRouter(
    prefix="/api/hang_man",
    tags=["Hang Man"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def hang_men_paginated(
            Limit: int = 10, Offset: int = 0, db: Session = Depends(get_db)
        ) -> HangManPaginatedResponse:
    count = db.query(HangMan).where(HangMan.Status != 1).count()
    items = []
    hang_men = db.query(HangMan).where(HangMan.Status != 1).order_by(
        HangMan.Status.desc(),
        HangMan.Score.desc()
    ).limit(Limit).offset(Offset).all()
    for hm in hang_men:
        items.append(hm.as_dict())
    return {"Count": count, "Limit": Limit, "Offset": Offset, "Items": items}

@router.get("/progress")
async def hang_men_in_progress(
            db: Session = Depends(get_db), user_id: Optional[str] = Depends(get_current_user)
        ) -> List[HangManResponse]:
    items = []
    if user_id is not None:
        hang_men = db.query(HangMan).where(HangMan.Status == 1).filter(HangMan.user_id == user_id).all()
        for hm in hang_men:
            items.append(hm.as_dict())
    return items

@router.get("/{hang_man_id}")
async def get_hang_man_by_id(hang_man_id: int, db: Session = Depends(get_db)) -> HangManResponse:
    hang_man = db.query(HangMan).where(HangMan.id == hang_man_id).first()
    if hang_man is None:
        raise HTTPException(status_code=404, detail="Hang Man not found")
    return hang_man.as_dict()

@router.post("/", status_code=201)
async def create_hang_man(
            body: HangManCreate, 
            db: Session = Depends(get_db), 
            user_id: Optional[str] = Depends(get_current_user)
        ) -> HangManResponse:
    hang_man = HangMan(
        word_id = body.WordId,
        Status = 1,
        Score = 0,
        Correct = "",
        Wrong = ""
    )
    if user_id is not None:
        hang_man.user_id = user_id
    db.add(hang_man)
    db.commit()
    db.refresh(hang_man)
    return hang_man.as_dict()

@router.post("/{hang_man_id}/guess")
async def hang_man_guess(
            hang_man_id: int, body: HangManGuess, db: Session = Depends(get_db)
        ) -> HangManGuessResponse:
    hang_man = db.query(HangMan).where(HangMan.id == hang_man_id).first()
    if hang_man is None:
        raise HTTPException(status_code=404, detail="Hang Man not found")
    correct = hang_man.Correct.split(",")
    wrong = hang_man.Wrong.split(",")
    word = list(body.Word)
    found: bool = ListContains(body.Letter,word)
    if found:
        correct.append(body.Letter)
    else:
        wrong.append(body.Letter)
    hang_man.Correct = ",".join(StringListUnique(correct))
    hang_man.Wrong = ",".join(StringListUnique(wrong))
    status = CalculateHangManStatus(word,correct,wrong) 
    if status != "Playing":
        hang_man.Status = GameStatusArray.index(status)
        hang_man.Score = CalculateHangManScore(word,correct,wrong,status)
    db.add(hang_man)
    db.commit()
    db.refresh(hang_man)
    return { "Letter": body.Letter, "Found": found }