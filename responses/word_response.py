from pydantic import BaseModel
from typing import Any

class WordResponse(BaseModel):
    id: int
    created_at: Any
    updated_at: Any
    Word: str
    Length: int
