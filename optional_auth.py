from fastapi.security.http import HTTPAuthorizationCredentials, HTTPBearer
from typing import Optional
from fastapi import Depends
import jwt
from dotenv import dotenv_values

optional_bearer = HTTPBearer(auto_error=False)

config = dotenv_values(".env")

async def get_current_user(auth: Optional[HTTPAuthorizationCredentials] = Depends(optional_bearer)):
    if auth is None:
        return None
    try:
        decoded = jwt.decode(auth.credentials, config["SECRET"], algorithms=["HS256"])
        if decoded["sub"]:
            return decoded["sub"]
    except:
        return None
    return None
