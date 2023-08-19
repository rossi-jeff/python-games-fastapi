from pydantic import BaseModel
from models.enums import Colors

class CodeBreakerGuessColorResponse(BaseModel):
    id: int
    created_at: str
    updated_at: str
    code_breaker_guess_id: int
    Color: Colors