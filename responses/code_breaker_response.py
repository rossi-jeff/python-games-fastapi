from pydantic import BaseModel
from typing import List, Any
from models.enums import GameStatus
from .user_response import UserResponse
from .code_breaker_code_response import CodeBreakerCodeResponse
from .code_breaker_guess_response import CodeBreakerGuessResponse

class CodeBreakerResponse(BaseModel):
    id: int
    created_at: Any
    updated_at: Any
    Columns: int
    Colors: int
    Score: int
    Available: str
    Status: GameStatus
    user_id: int | None

    user: UserResponse | None
    guesses: List[CodeBreakerGuessResponse] = []
    codes: List[CodeBreakerCodeResponse] = []

class CodeBreakerPaginatedResponse(BaseModel):
    Count: int
    Limit: int
    Offset: int
    Items: List[CodeBreakerResponse]
