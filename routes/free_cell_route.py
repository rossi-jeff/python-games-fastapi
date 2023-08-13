from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from models.free_cell import FreeCell
from sqlalchemy.orm import Session, joinedload
from payloads.free_cell_payload import FreeCellUpdate
from models.enums import GameStatusArray

router = APIRouter(
    prefix="/api/free_cell",
    tags=["Free Cell"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def free_cells_paginated(Limit: int = 10, Offset: int = 0, db: Session = Depends(get_db)):
    count = db.query(FreeCell).where(FreeCell.Status != 1).count()
    free_cells = db.query(FreeCell).where(FreeCell.Status != 1).order_by(
        FreeCell.Status.desc(),
        FreeCell.Moves.asc()
    ).limit(Limit).offset(Offset).options(joinedload(FreeCell.user)).all()
    items = []
    for cell in free_cells:
        items.append(cell.as_dict())
    return {"Count": count, "Limit": Limit, "Offset": Offset, "Items": items}

@router.get("/{free_cell_id}")
async def get_free_cell_by_id(free_cell_id: int, db: Session = Depends(get_db)):
    free_cell = db.query(FreeCell).where(FreeCell.id == free_cell_id).options(joinedload(FreeCell.user)).first()
    if free_cell is None:
        raise HTTPException(status_code=404, detail="Free Cell not found")
    return free_cell.as_dict()

@router.post("/")
async def create_free_cell(db: Session = Depends(get_db)):
    free_cell = FreeCell(
        Elapsed = 0,
        Moves = 0,
        Status = 1
    )
    db.add(free_cell)
    db.commit()
    db.refresh(free_cell)
    return free_cell.as_dict()

@router.patch("/{free_cell_id}")
async def update_free_cell(free_cell_id: int, body: FreeCellUpdate, db: Session = Depends(get_db)):
    free_cell = db.query(FreeCell).get(free_cell_id)
    if free_cell is None:
        raise HTTPException(status_code=404, detail="Free Cell not found")
    free_cell.Elapsed = body.Elapsed
    free_cell.Moves = body.Status
    free_cell.Status = GameStatusArray.index(body.Status.name)
    db.add(free_cell)
    db.commit()
    db.refresh(free_cell)
    return free_cell.as_dict()