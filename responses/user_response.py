from pydantic import BaseModel

class UserResponse(BaseModel):
    id: int
    created_at: str
    updated_at: str
    UserName: str
