from pydantic import BaseModel
from typing import List
from .ten_grand_score_response import TenGrandScoreResponse

class TenGrandTurnResponse(BaseModel):
    id: int
    created_at: str
    updated_at: str
    Score: int
    ten_grand_turn_id: int

    scores: List[TenGrandScoreResponse]
