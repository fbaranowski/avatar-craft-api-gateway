from pydantic import BaseModel


class CreateDeleteShare(BaseModel):
    to_user_email: str
    avatar_id: int
