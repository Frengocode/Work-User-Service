from pydantic import BaseModel
from typing import Optional


class SUser(BaseModel):

    id: int
    username: str
    picture_url: Optional[str] = None
    email: str

    age: int
    name: str
    surname: str
    role: str
    token: Optional[str] = None
    password: Optional[str] = None
