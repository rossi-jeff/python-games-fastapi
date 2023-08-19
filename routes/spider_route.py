from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from sqlalchemy.orm import Session, joinedload
from models.enums import GameStatusArray
from payloads.spider_payload import SpiderCreate, SpiderUpdate
from models.spider import Spider
from optional_auth import get_current_user
from typing import Optional
from responses.spider_response import SpiderResponse, SpiderPaginatedResponse

router = APIRouter(
    prefix="/api/spider",
    tags=["Spider"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def spiders_paginated(
            Limit: int = 10, Offset: int = 0, db: Session = Depends(get_db)
        ) -> SpiderPaginatedResponse:
    count = db.query(Spider).where(Spider.Status != 1).count()
    spiders = db.query(Spider).where(Spider.Status != 1).order_by(
        Spider.Status.desc(),
        Spider.Moves.asc()
    ).limit(Limit).offset(Offset).options(joinedload(Spider.user)).all()
    items = []
    for spider in spiders:
        items.append(spider.as_dict())
    return {"Count": count, "Limit": Limit, "Offset": Offset, "Items": items}

@router.get("/{spider_id}")
async def get_spider_by_id(
            spider_id: int, db: Session = Depends(get_db)
        ) -> SpiderResponse:
    spider = db.query(Spider).where(Spider.id == spider_id).options(joinedload(Spider.user)).first()
    if spider is None:
        raise HTTPException(status_code=404, detail="Spider not found")
    return spider.as_dict()

@router.post("/", status_code=201)
async def create_spider(
            body: SpiderCreate, 
            db: Session = Depends(get_db), 
            user_id: Optional[str] = Depends(get_current_user)
        ) -> SpiderResponse:
    spider = Spider(
        Suits = body.Suits.value,
        Elapsed = 0,
        Moves = 0,
        Status = 1
    )
    if user_id is not None:
        spider.user_id = user_id
    db.add(spider)
    db.commit()
    db.refresh(spider)
    return spider.as_dict()

@router.patch("/{spider_id}")
async def update_spider(
            spider_id: int, body: SpiderUpdate, db: Session = Depends(get_db)
        ) -> SpiderResponse:
    spider = db.query(Spider).where(Spider.id == spider_id).options(joinedload(Spider.user)).first()
    if spider is None:
        raise HTTPException(status_code=404, detail="Spider not found")
    spider.Moves = body.Moves
    spider.Elapsed = body.Elapsed
    spider.Status = GameStatusArray.index(body.Status.name)
    db.add(spider)
    db.commit()
    db.refresh(spider)
    return spider.as_dict()
