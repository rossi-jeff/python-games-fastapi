from pydantic import BaseModel
from models.enums import Keys
from typing import Any

class CodeBreakerGuessKeyResponse(BaseModel):
    id: int
    created_at: Any
    updated_at: Any
    code_breaker_guess_id: int
    Key: Keys
