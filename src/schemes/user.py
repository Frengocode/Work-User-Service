from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from typing import Optional
import uuid

class VacancyResponse(BaseModel):

    id: uuid.UUID
    work_category: str
    date_pub: datetime
    vacancy_title: str

    location: str
    description: str
    conditions: str

    price: int
    key_skils: str
    experience: int
    is_exist: bool
    user_id: Optional[int] = None


class UserResponse(BaseModel):
    
    id: int
    username: str
    
    joined_at: datetime
    picture_url: Optional[str] = None
    email: str
    
    age: int
    name: str
    surname: str
    role: str
    company_name: Optional[str] = None
    password: Optional[str] = None



class SelectRole(Enum):
    
    WORKER = "Работник"
    EMPLOYER = "Работодотель"









