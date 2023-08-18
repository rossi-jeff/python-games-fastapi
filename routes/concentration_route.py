from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from models.concentration import Concentration
from sqlalchemy.orm import Session, joinedload
from models.enums import GameStatusArray
from payloads.concentration_payload import ConcentrationUpdate
from optional_auth import get_current_user
from typing import Optional

router = APIRouter(
    prefix="/api/concentration",
    tags=["Concentration"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def concentrations_paginated(Limit: int = 10, Offset: int = 0, db: Session = Depends(get_db)):
    count = db.query(Concentration).where(Concentration.Status != 1).count()
    concentrations = db.query(Concentration).where(Concentration.Status != 1).order_by(
        Concentration.Status.desc(),
        Concentration.Moves.asc()
    ).limit(Limit).offset(Offset).options(joinedload(Concentration.user)).all()
    items = []
    for conc in concentrations:
        items.append(conc.as_dict())
    return {"Count": count, "Limit": Limit, "Offset": Offset, "Items": items}


@router.get("/{concentration_id}")
async def get_concentration_by_id(concentration_id: int, db: Session = Depends(get_db)):
    concentration = db.query(Concentration).where(Concentration.id == concentration_id).options(joinedload(Concentration.user)).first()
    if concentration is None:
        raise HTTPException(status_code=404, detail="Concentration not found")
    return concentration.as_dict()

@router.post("/")
async def create_concentration(db: Session = Depends(get_db), user_id: Optional[str] = Depends(get_current_user)):
    concentration = Concentration(
        Status = 1,
        Elapsed = 0,
        Moves = 0,
        Matched = 0
    )
    if user_id is not None:
        concentration.user_id = user_id
    db.add(concentration)
    db.commit()
    db.refresh(concentration)
    return concentration.as_dict()

@router.patch("/{concentration_id}")
async def update_concentration(concentration_id: int, body: ConcentrationUpdate, db: Session = Depends(get_db)):
    concentration = db.query(Concentration).where(Concentration.id == concentration_id).options(joinedload(Concentration.user)).first()
    if concentration is None:
        raise HTTPException(status_code=404, detail="Concentration not found")
    concentration.Elapsed = body.Elapsed
    concentration.Moves = body.Status
    concentration.Matched = body.Matched
    concentration.Status = GameStatusArray.index(body.Status.name)
    db.add(concentration)
    db.commit()
    db.refresh(concentration)
    return concentration.as_dict()