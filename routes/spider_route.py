from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from sqlalchemy.orm import Session, joinedload
from models.enums import GameStatusArray
from payloads.spider_payload import SpiderCreate, SpiderUpdate
from models.spider import Spider

router = APIRouter(
    prefix="/api/spider",
    tags=["Spider"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def spiders_paginated(Limit: int = 10, Offset: int = 0, db: Session = Depends(get_db)):
    count = db.query(Spider).where(Spider.Status != 1).count()
    items = db.query(Spider).where(Spider.Status != 1).order_by(
        Spider.Status.desc(),
        Spider.Moves.asc()
    ).limit(Limit).offset(Offset).options(joinedload(Spider.user)).all()
    return {"Count": count, "Limit": Limit, "Offset": Offset, "Items": items}

@router.get("/{spider_id}")
async def get_spider_by_id(spider_id: int, db: Session = Depends(get_db)):
    spider = db.query(Spider).where(Spider.id == spider_id).options(joinedload(Spider.user)).first()
    if spider is None:
        raise HTTPException(status_code=404, detail="Spider not found")
    return spider

@router.post("/")
async def create_spider(body: SpiderCreate, db: Session = Depends(get_db)):
    spider = Spider(
        Suits = body.Suits.value,
        Elapsed = 0,
        Moves = 0,
        Status = 1
    )
    db.add(spider)
    db.commit()
    db.refresh(spider)
    return spider

@router.patch("/{spider_id}")
async def update_spider(spider_id: int, body: SpiderUpdate, db: Session = Depends(get_db)):
    spider = db.query(Spider).where(Spider.id == spider_id).options(joinedload(Spider.user)).first()
    if spider is None:
        raise HTTPException(status_code=404, detail="Spider not found")
    spider.Moves = body.Moves
    spider.Elapsed = body.Elapsed
    spider.Status = GameStatusArray.index(body.Status.name)
    db.add(spider)
    db.commit()
    db.refresh(spider)
    return spider
