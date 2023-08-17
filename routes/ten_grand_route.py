from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from models.ten_grand import TenGrand
from sqlalchemy.orm import Session, joinedload
from models.ten_grand_turn import TenGrandTurn
from payloads.ten_grand_payload import TenGrandRoll, TenGrandOptions, TenGrandScorePayload
import random
from utilities.ten_grand import TenGrandScoreOptions, TGCategoryScoreAndDice, RemoveUsedDice
from models.ten_grand_turn import TenGrandTurn
from models.ten_grand_score import TenGrandScore
from models.enums import TenGrandDiceRequired, TenGrandCategoryArray

router = APIRouter(
    prefix="/api/ten_grand",
    tags=["Ten Grand"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def ten_grands_paginated(Limit: int = 10, Offset: int = 0, db: Session = Depends(get_db)):
    count = db.query(TenGrand).where(TenGrand.Status != 1).count()
    ten_grands = db.query(TenGrand).where(TenGrand.Status != 1).order_by(
        TenGrand.Status.desc(),
        TenGrand.Score.desc()
    ).limit(Limit).offset(Offset).all()
    items = []
    for tg in ten_grands:
        items.append(tg.as_dict())
    return {"Count": count, "Limit": Limit, "Offset": Offset, "Items": items}

@router.get("/{ten_grand_id}")
async def get_ten_grand_by_id(ten_grand_id: int, db: Session = Depends(get_db)):
    ten_grand = db.query(TenGrand).where(TenGrand.id == ten_grand_id).first()
    if ten_grand is None:
        raise HTTPException(status_code=404, detail="Ten Grand not found")
    return ten_grand.as_dict(True)

@router.post("/")
async def create_ten_grand(db: Session = Depends(get_db)):
    ten_grand = TenGrand(
        Score = 0,
        Status = 1
    )
    db.add(ten_grand)
    db.commit()
    db.refresh(ten_grand)
    return ten_grand.as_dict()

@router.post("/{ten_grand_id}/roll")
async def ten_grand_roll(ten_grand_id: int, body: TenGrandRoll):
    dice = []
    for idx in range(body.Quantity):
        dice.append(random.randint(1,6))
    return dice

@router.post("/options")
async def ten_grand_score_options(body: TenGrandOptions):
    return { "Dice": body.Dice, "Options": TenGrandScoreOptions(body.Dice) }

@router.post("/{ten_grand_id}/score")
async def ten_grand_score(ten_grand_id: int, body: TenGrandScorePayload, db: Session = Depends(get_db)):
    ten_grand = db.query(TenGrand).where(TenGrand.id == ten_grand_id).first()
    if ten_grand is None:
        raise HTTPException(status_code=404, detail="Ten Grand not found")
    turn = TenGrandTurn(
        ten_grand_id = ten_grand.id,
        Score = 0
    )
    if body.TurnId > 0:
        turn = db.query(TenGrandTurn).where(TenGrandTurn.id == body.TurnId).first()
    else:
        db.add(turn)
        db.commit()
        db.refresh(turn)
    dice = body.Dice
    options = body.Options
    options.sort(key=lambda o: TenGrandDiceRequired[o.Category.name], reverse=True)
    crapOut: bool = False
    for option in options:
        score, used = TGCategoryScoreAndDice(option.Category,dice)
        tgs = TenGrandScore(
            ten_grand_turn_id = turn.id,
            Score = score,
            Dice = ",".join(str(d) for d in used),
            Category = TenGrandCategoryArray.index(option.Category.name)
        )
        db.add(tgs)
        db.commit()
        dice = RemoveUsedDice(dice,used)
        turn.Score = turn.Score + score
        if option.Category.name == "CrapOut":
            crapOut = True
    if crapOut:
        turn.Score = 0
    db.add(turn)
    db.commit()
    db.refresh(turn)
    return turn.as_dict()
