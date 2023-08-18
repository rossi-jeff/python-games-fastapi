from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from sqlalchemy.orm import Session, joinedload
from models.yacht import Yacht
from models.yacht_turn import YachtTurn
from typing import List
from payloads.yacht_payload import YachtRoll, YachtScore
from utilities.yacht import YachtSkipCategories, YachtScoreOptions, StringToIntList, YachtCategoryScore, UpdateYachtTotal
from models.enums import YachtCategoryArray
import random
from optional_auth import get_current_user
from typing import Optional

router = APIRouter(
    prefix="/api/yacht",
    tags=["Yacht"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def yachts_paginated(Limit: int = 10, Offset: int = 0, db: Session = Depends(get_db)):
    count = db.query(Yacht).where(Yacht.NumTurns == 12).count()
    yachts = db.query(Yacht).where(Yacht.NumTurns == 12).order_by(
        Yacht.Total.desc()
		).limit(Limit).offset(Offset).all()
    items = []
    for y in yachts:
        items.append(y.as_dict())
    return {"Count": count, "Limit": Limit, "Offset": Offset, "Items": items}

@router.get("/progress")
async def yachts_in_progress(db: Session = Depends(get_db), user_id: Optional[str] = Depends(get_current_user)):
    items = []
    if user_id is not None:
        yachts = db.query(Yacht).where(Yacht.NumTurns < 12).filter(Yacht.user_id == user_id).all()
        for y in yachts:
            items.append(y.as_dict())
    return items

@router.get("/{yacht_id}")
async def get_yacht_by_id(yacht_id: int, db: Session = Depends(get_db)):
    yacht = db.query(Yacht).where(Yacht.id == yacht_id).first()
    if yacht is None:
        raise HTTPException(status_code=404, detail="Yacht not found")
    return yacht.as_dict(True)

@router.post("/")
async def create_yacht(db: Session = Depends(get_db), user_id: Optional[str] = Depends(get_current_user)):
    yacht = Yacht(
        Total = 0,
        NumTurns = 0
		)
    if user_id is not None:
        yacht.user_id = user_id
    db.add(yacht)
    db.commit()
    db.refresh(yacht)
    return yacht.as_dict()

@router.post("/{yacht_id}/roll")
async def yacht_roll(yacht_id: int, body: YachtRoll, db: Session = Depends(get_db)):
    dice: list[int] = []
    for k in body.Keep:
        dice.append(k)
    while len(dice) < 5:
        dice.append(random.randint(1,6))
    skip = YachtSkipCategories(db,yacht_id)
    options = YachtScoreOptions(dice,skip)
    turn = db.query(YachtTurn).where(YachtTurn.yacht_id == yacht_id).filter(YachtTurn.Category == None).first()
    if turn is None:
        turn = YachtTurn(
            yacht_id = yacht_id,
            RollOne = ",".join(str(d) for d in dice),
            RollTwo = "",
            RollThree = "",
            Score = 0
        )
    else:
        if turn.RollTwo != "":
            turn.RollThree = ",".join(str(d) for d in dice)
        else:
            turn.RollTwo = ",".join(str(d) for d in dice)
    db.add(turn)
    db.commit()
    db.refresh(turn)
    return { "Turn": turn.as_dict(), "Options": options }

@router.post("/{yacht_id}/score")
def yacht_score_turn(yacht_id: int, body: YachtScore, db: Session = Depends(get_db)):
    turn = db.query(YachtTurn).where(YachtTurn.id == body.TurnId).first()
    if turn is None:
        raise HTTPException(status_code=404, detail="Yacht Turn not found")
    dice: List[int] = []
    if turn.RollThree != "":
        dice = StringToIntList(turn.RollThree)
    elif turn.RollTwo != "":
        dice = StringToIntList(turn.RollTwo)
    else:
        dice = StringToIntList(turn.RollOne)
    turn.Score = YachtCategoryScore(body.Category,dice)
    turn.Category = YachtCategoryArray.index(body.Category.name)
    db.add(turn)
    db.commit()
    db.refresh(turn)
    UpdateYachtTotal(db,yacht_id)
    return turn.as_dict()
