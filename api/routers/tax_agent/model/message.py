

from pydantic import BaseModel


class UserMessage(BaseModel):
    message: str
    session_id: str


class AIResponse(BaseModel):
    message: str
    session_id: str
