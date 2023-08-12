from fastapi import APIRouter, Depends
from database import get_db
from models.free_cell import FreeCell
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/api/free_cell",
    tags=["Free Cell"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def free_cells_paginated(Limit: int = 10, Offset: int = 0, db: Session = Depends(get_db)):
    count = db.query(FreeCell).where(FreeCell.Status != 1).count()
    items = db.query(FreeCell).where(FreeCell.Status != 1).order_by(
        FreeCell.Status.desc(),
        FreeCell.Moves.asc()
    ).limit(Limit).offset(Offset).all()
    return {"Count": count, "Limit": Limit, "Offset": Offset, "Items": items}

@router.get("/{free_cell_id}")
async def get_free_cell_by_id(free_cell_id: int):
    return {"message": "TODO"}

@router.post("/")
async def create_free_cell():
    return {"message": "TODO"}

@router.patch("/{free_cell_id}")
async def update_free_cell(free_cell_id: int):
    return {"message": "TODO"}