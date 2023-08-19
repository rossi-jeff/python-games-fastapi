from pydantic import BaseModel
from models.enums import YachtCategory

class YachtTurnResponse(BaseModel):
    id: int
    created_at: str
    updated_at: str
    RollOne: str
    RollTwo: str
    RollThree: str
    Score: int
    Category: YachtCategory | None
    yacht_id: int
