from fastapi import Depends, status, HTTPException
from src.uitils.scheme import SUser
from sqlalchemy.ext.asyncio import AsyncSession
from src.config.database import async_session
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
import httpx
from fastapi.security import OAuth2PasswordBearer


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 365


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth-login/")
pwd_context = CryptContext(schemes=["bcrypt"])


class Uitils:

    async def get_user_session() -> AsyncSession:
        async with async_session() as session:
            try:
                yield session
            finally:
                await session.close()

    def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt


class Hash:

    @staticmethod
    def bcrypt(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)


