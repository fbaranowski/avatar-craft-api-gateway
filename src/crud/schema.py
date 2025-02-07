from pydantic import BaseModel


class CreateAvatar(BaseModel):
    ai_model: str
    prompt: str


class DeleteAvatar(BaseModel):
    avatar_id: int
