from pydantic import BaseModel
from models.enums import Keys

class CodeBreakerGuessKeyResponse(BaseModel):
    id: int
    created_at: str
    updated_at: str
    code_breaker_guess_id: int
    Key: Keys
