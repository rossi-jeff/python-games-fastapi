from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from sqlalchemy.orm import Session, joinedload
from models.enums import GameStatusArray
from payloads.poker_square_payload import PokerSquareUpdate
from models.poker_square import PokerSquare

router = APIRouter(
    prefix="/api/poker_square",
    tags=["Poker Square"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def poker_squares_paginated(Limit: int = 10, Offset: int = 0, db: Session = Depends(get_db)):
    count = db.query(PokerSquare).where(PokerSquare.Status != 1).count()
    items = db.query(PokerSquare).where(PokerSquare.Status != 1).order_by(
        PokerSquare.Status.desc(),
        PokerSquare.Score.asc()
    ).limit(Limit).offset(Offset).options(joinedload(PokerSquare.user)).all()
    return {"Count": count, "Limit": Limit, "Offset": Offset, "Items": items}

@router.get("/{poker_square_id}")
async def get_poker_square_by_id(poker_square_id: int, db: Session = Depends(get_db)):
    poker_square = db.query(PokerSquare).where(PokerSquare.id == poker_square_id).options(joinedload(PokerSquare.user)).first()
    if poker_square is None:
        raise HTTPException(status_code=404, detail="Poker Square not found")
    return poker_square

@router.post("/")
async def create_poker_square(db: Session = Depends(get_db)):
    poker_square = PokerSquare(
        Score = 0,
        Status = 1
    )
    db.add(poker_square)
    db.commit()
    db.refresh(poker_square)
    return poker_square

@router.patch("/{poker_square_id}")
async def update_poker_square(poker_square_id: int, body: PokerSquareUpdate, db: Session = Depends(get_db)):
    poker_square = db.query(PokerSquare).where(PokerSquare.id == poker_square_id).options(joinedload(PokerSquare.user)).first()
    if poker_square is None:
        raise HTTPException(status_code=404, detail="Poker Square not found")
    poker_square.Score = body.Score
    poker_square.Status = GameStatusArray.index(body.Status.name)
    db.add(poker_square)
    db.commit()
    db.refresh(poker_square)
    return poker_square
