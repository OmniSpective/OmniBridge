from pydantic import BaseModel


class AIModel(BaseModel):
    id: int
    name: str
    type: str
    description: str
