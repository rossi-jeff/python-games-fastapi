from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from models.ten_grand import TenGrand
from sqlalchemy.orm import Session, joinedload
from models.ten_grand_turn import TenGrandTurn

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
