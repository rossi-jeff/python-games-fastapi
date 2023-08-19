from pydantic import BaseModel
from models.enums import Colors

class CodeBreakerCodeResponse(BaseModel):
    id: int
    created_at: str
    updated_at: str
    code_breaker_id: int
    Color: Colors
