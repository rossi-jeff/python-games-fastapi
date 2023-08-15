from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from models.sea_battle import SeaBattle
from sqlalchemy.orm import Session, joinedload
from payloads.sea_battle_payload import SeaBattleCreate, SeaBattleShipPayload, SeaBattleFire
from models.sea_battle_ship import SeaBattleShip
from models.enums import ShipTypeArray, NavyArray

router = APIRouter(
    prefix="/api/sea_battle",
    tags=["Sea Battle"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def sea_battles_paginated(Limit: int = 10, Offset: int = 0, db: Session = Depends(get_db)):
    count = db.query(SeaBattle).where(SeaBattle.Status != 1).count()
    sea_battles = db.query(SeaBattle).where(SeaBattle.Status != 1).order_by(
        SeaBattle.Status.desc(),
        SeaBattle.Score.desc()
    ).limit(Limit).offset(Offset).all()
    items = []
    for sb in sea_battles:
        items.append(sb.as_dict())
    return {"Count": count, "Limit": Limit, "Offset": Offset, "Items": items}

@router.get("/{sea_battle_id}")
async def get_sea_battle_by_id(sea_battle_id: int, db: Session = Depends(get_db)):
    sea_battle = db.query(SeaBattle).where(SeaBattle.id == sea_battle_id).first()
    if sea_battle is None:
        raise HTTPException(status_code=404, detail="Sea Battle not found")
    return sea_battle.as_dict(True)

@router.post("/")
async def create_sea_battle(body: SeaBattleCreate, db: Session = Depends(get_db)):
    sea_battle = SeaBattle(
        Axis = body.Axis,
        Status = 1,
        Score = 0
    )
    db.add(sea_battle)
    db.commit()
    db.refresh(sea_battle)
    return sea_battle.as_dict()

@router.post("/{sea_battle_id}/ship")
async def sea_battle_create_ship(sea_battle_id: int, body: SeaBattleShipPayload, db: Session = Depends(get_db)):
    sea_battle = db.query(SeaBattle).where(SeaBattle.id == sea_battle_id).first()
    if sea_battle is None:
        raise HTTPException(status_code=404, detail="Sea Battle not found")
    sea_battle_ship = SeaBattleShip(
        sea_battle_id = sea_battle_id,
        Navy = NavyArray.index(body.Navy.name),
        Type = ShipTypeArray.index(body.ShipType.name),
        Size = body.Size,
        Sunk = False
    )
    return { "message": "TODO" }

@router.post("/{sea_battle_id}/fire")
async def sea_battle_fire(sea_battle_id: int, body: SeaBattleFire, db: Session = Depends(get_db)):
    sea_battle = db.query(SeaBattle).where(SeaBattle.id == sea_battle_id).first()
    if sea_battle is None:
        raise HTTPException(status_code=404, detail="Sea Battle not found")
    return { "message": "TODO" }
