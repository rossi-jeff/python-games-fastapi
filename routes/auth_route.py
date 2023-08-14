from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from models.user import User
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
    user = User(
        UserName = body.UserName,
        password_digest = bcrypt.hashpw(body.password.encode('utf8'), bcrypt.gensalt())
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/login")
async def login(body: AuthCredentials, db: Session = Depends(get_db)):
    user = db.query(User).where(User.UserName == body.UserName).first()
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