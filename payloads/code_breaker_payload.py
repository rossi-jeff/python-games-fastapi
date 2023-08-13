from pydantic import BaseModel
from models.enums import Colors
from typing import List

class CodeBreakerCreate(BaseModel):
    Columns: int | None = None
    Colors: List[Colors]

class CodeBreakerGuessPayload(BaseModel):
    Colors: List[Colors]