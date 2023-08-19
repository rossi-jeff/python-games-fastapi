from pydantic import BaseModel
from typing import Any

class UserResponse(BaseModel):
    id: int
    created_at: Any
    updated_at: Any
    UserName: str
