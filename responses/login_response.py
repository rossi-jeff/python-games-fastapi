from pydantic import BaseModel

class LoginResponse(BaseModel):
    UserName: str
    Token: str
