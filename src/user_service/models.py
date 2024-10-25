from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean, DateTime
from datetime import datetime
from src.config.database import UserBase
from sqlalchemy.dialects.postgresql import UUID
import uuid


class User(UserBase):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, index = True, primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)

    name: Mapped[str]  = mapped_column(String, nullable=False)
    surname: Mapped[str]  = mapped_column(String, nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)

    password: Mapped[str] = mapped_column(String, nullable=False)
    joined_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    picture_url: Mapped[str] = mapped_column(String, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    role: Mapped[str] = mapped_column(String, nullable=False)
    company_name: Mapped[str] = mapped_column(String, nullable=True)
    password_reset_tok: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=True, default=uuid.uuid4)
