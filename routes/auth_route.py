from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from models.user import User, UserDB
from payloads.auth_payload import AuthCredentials
from sqlalchemy.orm import Session
import bcrypt
import jwt
from dotenv import dotenv_values
from datetime import datetime, timedelta

# jwt.decode(encoded_jwt, "secret", algorithms=["HS256"])

WEEK = 60 * 60 * 24 * 7 * 1000

config = dotenv_values(".env")

router = APIRouter(
    prefix="/api/auth",
    tags=["Auth"],
    responses={404: {"description": "Not found"}},
)

@router.post("/register")
async def register(body: AuthCredentials, db: Session = Depends(get_db)):
    user_db = UserDB(
        UserName = body.UserName,
        password_digest = bcrypt.hashpw(body.password.encode('utf8'), bcrypt.gensalt())
    )
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    user = db.query(User).where(User.id == user_db.id).first()
    return user

@router.post("/login")
async def login(body: AuthCredentials, db: Session = Depends(get_db)):
    user = db.query(UserDB).where(UserDB.UserName == body.UserName).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    if not bcrypt.checkpw(body.password.encode('utf8'), user.password_digest.encode('utf8')):
        raise HTTPException(status_code=401, detail="Unauthorized")
    payload = {
        "sub": user.id,
        "iat": datetime.utcnow().timestamp(),
        "exp": datetime.utcnow().timestamp() + WEEK
    }
    token = jwt.encode(payload, config["SECRET"], algorithm="HS256")
    return { "UserName": body.UserName, "Token": token}