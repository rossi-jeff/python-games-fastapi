from fastapi import APIRouter, HTTPException, Depends
from payloads.random_word_payload import RandomWordPayload
from database import get_db
from models.word import Word
from sqlalchemy.sql.expression import func
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/api/word",
    tags=["Word"],
    responses={404: {"description": "Not found"}},
)

@router.post("/random")
async def get_random_word(body: RandomWordPayload, db: Session = Depends(get_db)):
    if body.Length > 0:
        word = db.query(Word).where(Word.Length == body.Length).order_by(func.rand()).limit(1).first()
    elif body.Max > 0 and body.Min > 0 : 
        word = db.query(Word).where(Word.Length.between(body.Min,body.Max)).order_by(func.rand()).limit(1).first()
    
    if word is None:
         raise HTTPException(status_code=404, detail="Word not found")
    return word

@router.get("/{word_id}")
async def get_word_by_id(word_id: int, db: Session = Depends(get_db)):
    word = db.query(Word).get(word_id)
    if word is None:
         raise HTTPException(status_code=404, detail="Word not found")
    return word
