from typing import List
from pydantic import BaseModel


class CreateAvatar(BaseModel):
    email: str
    ai_model: str
    prompt: str


class EditAvatar(BaseModel):
    email: str
    avatars_urls: List[str]
    ai_model: str
    prompt: str


class DeleteAvatar(BaseModel):
    email: str
    avatar_id: int
