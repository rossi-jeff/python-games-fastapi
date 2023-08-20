from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from models.sea_battle import SeaBattle
from sqlalchemy.orm import Session, joinedload
from payloads.sea_battle_payload import SeaBattleCreate, SeaBattleShipPayload, SeaBattleFire, SeaBattlePoint
from models.sea_battle_ship import SeaBattleShip
from models.enums import ShipTypeArray, NavyArray, Navy, Target, ShipType, TargetArray
from models.sea_battle_ship_grid_point import SeaBattleShipGridPoint
from utilities.sea_battle import OpponentShipPoints, OpponentFirePoint, SeaBattleStatus, UpdateSeaBattle
from models.sea_battle_ship_hit import SeabattleShipHit
from models.sea_battle_turn import SeaBattleTurn
from optional_auth import get_current_user
from typing import Optional, List
from responses.sea_battle_response import SeaBattleResponse, SeaBattlePaginatedResponse
from responses.sea_battle_ship_response import SeaBattleShipResponse
from responses.sea_battle_turn_response import SeaBattleTurnResponse

router = APIRouter(
    prefix="/api/sea_battle",
    tags=["Sea Battle"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def sea_battles_paginated(
    Limit: int = 10, Offset: int = 0, db: Session = Depends(get_db)
) -> SeaBattlePaginatedResponse:
    count = db.query(SeaBattle).where(SeaBattle.Status != 1).count()
    sea_battles = db.query(SeaBattle).where(SeaBattle.Status != 1).order_by(
        SeaBattle.Status.desc(),
        SeaBattle.Score.desc()
    ).limit(Limit).offset(Offset).all()
    items = []
    for sb in sea_battles:
        items.append(sb.as_dict())
    return {"Count": count, "Limit": Limit, "Offset": Offset, "Items": items}


@router.get("/progress")
async def sea_battles_in_progress(
    db: Session = Depends(get_db), user_id: Optional[str] = Depends(get_current_user)
) -> List[SeaBattleResponse]:
    items = []
    if user_id is not None:
        sea_battles = db.query(SeaBattle).where(
            SeaBattle.Status == 1).filter(SeaBattle.user_id == user_id).all()
        for sb in sea_battles:
            items.append(sb.as_dict())
    return items


@router.get("/{sea_battle_id}")
async def get_sea_battle_by_id(
    sea_battle_id: int, db: Session = Depends(get_db)
) -> SeaBattleResponse:
    sea_battle = db.query(SeaBattle).where(
        SeaBattle.id == sea_battle_id).first()
    if sea_battle is None:
        raise HTTPException(status_code=404, detail="Sea Battle not found")
    return sea_battle.as_dict(True)


@router.post("/", status_code=201)
async def create_sea_battle(
    body: SeaBattleCreate,
    db: Session = Depends(get_db),
    user_id: Optional[str] = Depends(get_current_user)
) -> SeaBattleResponse:
    sea_battle = SeaBattle(
        Axis=body.Axis,
        Status=1,
        Score=0
    )
    if user_id is not None:
        sea_battle.user_id = user_id
    db.add(sea_battle)
    db.commit()
    db.refresh(sea_battle)
    return sea_battle.as_dict()


@router.post("/{sea_battle_id}/ship", status_code=201)
async def sea_battle_create_ship(
    sea_battle_id: int, body: SeaBattleShipPayload, db: Session = Depends(get_db)
) -> SeaBattleShipResponse:
    sea_battle = db.query(SeaBattle).where(
        SeaBattle.id == sea_battle_id).first()
    if sea_battle is None:
        raise HTTPException(status_code=404, detail="Sea Battle not found")
    sea_battle_ship = SeaBattleShip(
        sea_battle_id=sea_battle_id,
        Navy=NavyArray.index(body.Navy.name),
        Type=ShipTypeArray.index(body.ShipType.name),
        Size=body.Size,
        Sunk=False
    )
    db.add(sea_battle_ship)
    db.commit()
    db.refresh(sea_battle_ship)
    if body.Navy == Navy.Player:
        for point in body.Points:
            sbsgp = SeaBattleShipGridPoint(
                sea_battle_ship_id=sea_battle_ship.id,
                Horizontal=point.Horizontal,
                Vertical=point.Vertical
            )
            db.add(sbsgp)
            db.commit()
    else:
        points = OpponentShipPoints(
            db, sea_battle_id, sea_battle.Axis, body.Size)
        for point in points:
            sbsgp = SeaBattleShipGridPoint(
                sea_battle_ship_id=sea_battle_ship.id,
                Horizontal=point["Horizontal"],
                Vertical=point["Vertical"]
            )
            db.add(sbsgp)
            db.commit()
    db.refresh(sea_battle_ship)
    return sea_battle_ship.as_dict()


@router.post("/{sea_battle_id}/fire", status_code=201)
async def sea_battle_fire(
    sea_battle_id: int, body: SeaBattleFire, db: Session = Depends(get_db)
) -> SeaBattleTurnResponse:
    sea_battle = db.query(SeaBattle).where(
        SeaBattle.id == sea_battle_id).first()
    if sea_battle is None:
        raise HTTPException(status_code=404, detail="Sea Battle not found")
    point: SeaBattlePoint | None = None
    if body.Navy == Navy.Player:
        point = SeaBattlePoint(
            Horizontal=body.Horizontal,
            Vertical=body.Vertical
        )
    else:
        point = OpponentFirePoint(db, sea_battle_id, sea_battle.Axis)
    target: Target = Target.Miss
    shipType: int | None = None
    ships = db.query(SeaBattleShip).where(
        SeaBattleShip.sea_battle_id == sea_battle_id
    ).filter(SeaBattleShip.Navy != NavyArray.index(body.Navy.name)).all()
    for ship in ships:
        for p in ship.points:
            if point.Horizontal == p.Horizontal and point.Vertical == p.Vertical:
                if len(ship.hits) + 1 >= len(ship.points):
                    target = Target.Sunk
                else:
                    target = Target.Hit
                shipType = ship.Type
                hit = SeabattleShipHit(
                    sea_battle_ship_id=ship.id,
                    Horizontal=point.Horizontal,
                    Vertical=point.Vertical
                )
                db.add(hit)
                db.commit()
                if target == Target.Sunk:
                    ship.Sunk = True
                    db.add(ship)
                    db.commit()
    turn = SeaBattleTurn(
        sea_battle_id=sea_battle_id,
        Navy=NavyArray.index(body.Navy.name),
        Target=TargetArray.index(target.name),
        ShipType=shipType,
        Horizontal=point.Horizontal,
        Vertical=point.Vertical
    )
    db.add(turn)
    db.commit()
    db.refresh(turn)
    status = SeaBattleStatus(db, sea_battle_id)
    print("status", status.name)
    if status.name != "Playing":
        UpdateSeaBattle(db, sea_battle_id, status)
    return turn.as_dict()
