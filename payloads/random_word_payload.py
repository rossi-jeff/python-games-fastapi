from pydantic import BaseModel

class RandomWordPayload(BaseModel):
    Length: int | None = None
    Min: int | None = None
    Max: int | None = None
    