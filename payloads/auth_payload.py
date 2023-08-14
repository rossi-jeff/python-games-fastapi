from pydantic import BaseModel

class AuthCredentials(BaseModel):
    UserName: str
    password: str