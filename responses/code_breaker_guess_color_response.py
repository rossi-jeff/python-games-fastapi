from pydantic import BaseModel
from models.enums import Colors
from typing import Any

class CodeBreakerGuessColorResponse(BaseModel):
    id: int
    created_at: Any
    updated_at: Any
    code_breaker_guess_id: int
    Color: Colors