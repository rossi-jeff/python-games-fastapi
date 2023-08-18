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
    decoded = jwt.decode(auth.credentials, config["SECRET"], algorithms=["HS256"])
    if decoded["sub"]:
        return decoded["sub"]
    return None

"""
{
  "UserName": "PythonUser",
  "Token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjksImV4cCI6MjI5NzE4NjE3OS41MTQyOTl9.L4_ongIiJfPtBOhMPju4rP6vd7B0TQLuihVPOrfLV-Y"
}
"""