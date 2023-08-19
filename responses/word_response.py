from pydantic import BaseModel

class WordResponse(BaseModel):
    id: int
    created_at: str
    updated_at: str
    Word: str
    Length: int
