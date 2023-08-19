from pydantic import BaseModel
from typing import List, Any
from .ten_grand_score_response import TenGrandScoreResponse


class TenGrandTurnResponse(BaseModel):
    id: int
    created_at: Any
    updated_at: Any
    Score: int
    ten_grand_id: int

    scores: List[TenGrandScoreResponse] = []
