from pydantic import BaseModel
from typing import List
from .code_breaker_guess_color_response import CodeBreakerGuessColorResponse
from .code_breaker_guess_key_response import CodeBreakerGuessKeyResponse

class CodeBreakerGuessResponse(BaseModel):
    id: int
    created_at: str
    updated_at: str
    code_breaker_id: int

    colors: List[CodeBreakerGuessColorResponse]
    keys: List[CodeBreakerGuessKeyResponse]
