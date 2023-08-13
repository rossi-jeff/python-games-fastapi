from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from sqlalchemy.orm import Session, joinedload
from models.enums import GameStatusArray
from payloads.klondike_payload import KlondikeUpdate
from models.klondike import Klondike

router = APIRouter(
    prefix="/api/klondike",
    tags=["Klondike"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def klondikes_paginated(Limit: int = 10, Offset: int = 0, db: Session = Depends(get_db)):
    count = db.query(Klondike).where(Klondike.Status != 1).count()
    klondikes = db.query(Klondike).where(Klondike.Status != 1).order_by(
        Klondike.Status.desc(),
        Klondike.Moves.asc()
    ).limit(Limit).offset(Offset).options(joinedload(Klondike.user)).all()
    items = []
    for klondike in klondikes:
        items.append(klondike.as_dict())
    return {"Count": count, "Limit": Limit, "Offset": Offset, "Items": items}

@router.get("/{klondike_id}")
async def get_klondike_by_id(klondike_id: int, db: Session = Depends(get_db)):
    klondike = db.query(Klondike).where(Klondike.id == klondike_id).options(joinedload(Klondike.user)).first()
    if klondike is None:
        raise HTTPException(status_code=404, detail="Klondike not found")
    return klondike.as_dict()

@router.post("/")
async def create_klondike(db: Session = Depends(get_db)):
    klondike = Klondike(
        Elapsed = 0,
        Moves = 0,
        Status = 1
    )
    db.add(klondike)
    db.commit()
    db.refresh(klondike)
    return klondike.as_dict()

@router.patch("/{klondike_id}")
async def update_klondike(klondike_id: int, body: KlondikeUpdate, db: Session = Depends(get_db)):
    klondike = db.query(Klondike).where(Klondike.id == klondike_id).options(joinedload(Klondike.user)).first()
    if klondike is None:
        raise HTTPException(status_code=404, detail="Klondike not found")
    klondike.Elapsed = body.Elapsed
    klondike.Moves = body.Status
    klondike.Status = GameStatusArray.index(body.Status.name)
    db.add(klondike)
    db.commit()
    db.refresh(klondike)
    return klondike.as_dict()