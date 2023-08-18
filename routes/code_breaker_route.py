from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from models.code_breaker import CodeBreaker 
from sqlalchemy.orm import Session, joinedload
from payloads.code_breaker_payload import CodeBreakerCreate, CodeBreakerGuessPayload
from models.code_breaker_code import CodeBreakerCode
from models.code_breaker_guess import CodeBreakerGuess
from models.code_breaker_code import CodeBreakerCode
from models.enums import ColorsArray, GameStatusArray
from models.code_breaker_guess_color import CodeBreakerGuessColor
from models.code_breaker_guess_keys import CodeBreakerGuessKey
from utilities.code_breaker import CalculateGuessKeys, CalculateCodeBreakerStatus, CalculateCodeBreakerScore
import random
from optional_auth import get_current_user
from typing import Optional

router = APIRouter(
    prefix="/api/code_breaker",
    tags=["Code Breaker"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def code_breakers_paginated(Limit: int = 10, Offset: int = 0, db: Session = Depends(get_db)):
    count = db.query(CodeBreaker).where(CodeBreaker.Status != 1).count()
    code_breakers = db.query(CodeBreaker).where(CodeBreaker.Status != 1).order_by(
        CodeBreaker.Status.desc(),
        CodeBreaker.Score.desc()
    ).limit(Limit).offset(Offset).all()
    items = []
    for cb in code_breakers:
        items.append(cb.as_dict())
    return {"Count": count, "Limit": Limit, "Offset": Offset, "Items": items}

@router.get("/progress")
async def code_breakers_in_progress(db: Session = Depends(get_db), user_id: Optional[str] = Depends(get_current_user)):
    items = []
    if user_id is not None:
        code_breakers = db.query(CodeBreaker).where(CodeBreaker.Status == 1).filter(CodeBreaker.user_id == user_id).all()
        for cb in code_breakers:
            items.append(cb.as_dict())
    return items

@router.get("/{code_breaker_id}")
async def get_code_breaker_by_id(code_breaker_id: int, db: Session = Depends(get_db)):
    code_breaker = db.query(CodeBreaker).where(CodeBreaker.id == code_breaker_id).first()
    if code_breaker is None:
        raise HTTPException(status_code=404, detail="Code Breaker not found")
    return code_breaker.as_dict(True)


@router.post("/")
async def create_code_breaker(body: CodeBreakerCreate, db: Session = Depends(get_db), user_id: Optional[str] = Depends(get_current_user)):
    s = ","
    colors = []
    for c in body.Colors:
        colors.append(c.name)
    code_breaker = CodeBreaker(
        Status = 1,
        Columns = body.Columns,
        Available = s.join(colors),
        Colors = len(colors),
        Score = 0
    )
    if user_id is not None:
        code_breaker.user_id = user_id
    db.add(code_breaker)
    db.commit()
    db.refresh(code_breaker)
    for x in range(body.Columns):
        color = random.choice(body.Colors)
        code = CodeBreakerCode(
            code_breaker_id = code_breaker.id,
            Color = ColorsArray.index(color.name)
        )
        db.add(code)
        db.commit()
    db.refresh(code_breaker)
    return code_breaker.as_dict(True)

@router.post("/{code_breaker_id}/guess")
async def take_code_breaker_guess(code_breaker_id: int, body: CodeBreakerGuessPayload, db: Session = Depends(get_db)):
    code_breaker_guess = CodeBreakerGuess(
        code_breaker_id = code_breaker_id
    )
    db.add(code_breaker_guess)
    db.commit()
    db.refresh(code_breaker_guess)
    guess = []
    for color in body.Colors:
        guess.append(color.name)
        cbgc = CodeBreakerGuessColor(
            code_breaker_guess_id = code_breaker_guess.id,
            Color = ColorsArray.index(color.name)
        )
        db.add(cbgc)
        db.commit()
    solution = []
    codes = db.query(CodeBreakerCode).where(CodeBreakerCode.code_breaker_id == code_breaker_id).all()
    for code in codes:
        solution.append(ColorsArray[code.Color])
    black, white = CalculateGuessKeys(guess,solution)
    if black > 0:
        for x in range(black):
            key = CodeBreakerGuessKey(
                code_breaker_guess_id = code_breaker_guess.id,
                Key = 0
            )
            db.add(key)
            db.commit()
    if white > 0:
        for x in range(white):
            key = CodeBreakerGuessKey(
                code_breaker_guess_id = code_breaker_guess.id,
                Key = 1
            )
            db.add(key)
            db.commit()
    db.refresh(code_breaker_guess)
    code_breaker = db.query(CodeBreaker).where(CodeBreaker.id == code_breaker_id).first()
    count = db.query(CodeBreakerGuess).where(CodeBreakerGuess.code_breaker_id == code_breaker_id).count()
    status = CalculateCodeBreakerStatus(black,code_breaker.Columns,count)
    if status != "Playing":
        code_breaker.Status = GameStatusArray.index(status)
        code_breaker.Score = CalculateCodeBreakerScore(db,code_breaker_id,code_breaker.Columns,code_breaker.Colors)
        db.add(code_breaker)
        db.commit()
    return code_breaker_guess.as_dict()
