from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from sqlalchemy.orm import Session, joinedload
from models.enums import GameStatusArray
from payloads.poker_square_payload import PokerSquareUpdate
from models.poker_square import PokerSquare
from optional_auth import get_current_user
from typing import Optional
from responses.poker_square_response import PokerSquareResponse, PokerSquarePaginatedResponse

router = APIRouter(
    prefix="/api/poker_square",
    tags=["Poker Square"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def poker_squares_paginated(
            Limit: int = 10, Offset: int = 0, db: Session = Depends(get_db)
        ) -> PokerSquarePaginatedResponse:
    count = db.query(PokerSquare).where(PokerSquare.Status != 1).count()
    poker_squares = db.query(PokerSquare).where(PokerSquare.Status != 1).order_by(
        PokerSquare.Status.desc(),
        PokerSquare.Score.asc()
    ).limit(Limit).offset(Offset).options(joinedload(PokerSquare.user)).all()
    items = []
    for square in poker_squares:
        items.append(square.as_dict())
    return {"Count": count, "Limit": Limit, "Offset": Offset, "Items": items}

@router.get("/{poker_square_id}")
async def get_poker_square_by_id(
            poker_square_id: int, db: Session = Depends(get_db)
        ) -> PokerSquareResponse:
    poker_square = db.query(PokerSquare).where(PokerSquare.id == poker_square_id).options(joinedload(PokerSquare.user)).first()
    if poker_square is None:
        raise HTTPException(status_code=404, detail="Poker Square not found")
    return poker_square

@router.post("/", status_code=201)
async def create_poker_square(
            db: Session = Depends(get_db), user_id: Optional[str] = Depends(get_current_user)
        ) -> PokerSquareResponse:
    poker_square = PokerSquare(
        Score = 0,
        Status = 1
    )
    if user_id is not None:
        poker_square.user_id = user_id
    db.add(poker_square)
    db.commit()
    db.refresh(poker_square)
    return poker_square.as_dict()

@router.patch("/{poker_square_id}")
async def update_poker_square(
            poker_square_id: int, body: PokerSquareUpdate, db: Session = Depends(get_db)
        ) -> PokerSquareResponse:
    poker_square = db.query(PokerSquare).where(PokerSquare.id == poker_square_id).options(joinedload(PokerSquare.user)).first()
    if poker_square is None:
        raise HTTPException(status_code=404, detail="Poker Square not found")
    poker_square.Score = body.Score
    poker_square.Status = GameStatusArray.index(body.Status.name)
    db.add(poker_square)
    db.commit()
    db.refresh(poker_square)
    return poker_square.as_dict()
