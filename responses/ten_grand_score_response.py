from pydantic import BaseModel
from models.enums import TenGrandCategory

class TenGrandScoreResponse(BaseModel):
    id: int
    created_at: str
    updated_at: str
    Dice: str
    Score: int
    Category: TenGrandCategory
    ten_grand_turn_id: int
