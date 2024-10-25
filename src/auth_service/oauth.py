from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from src.uitils.scheme import SUser
import httpx
# from src.requests.request import AUTH_REQUEST, GET_CURRENT_USER_REQUEST

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "auth-login/")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> SUser:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"http://192.168.100.59:8000/user-service/api/v1/get-current-user/{user_id}/"
        )


        if response.status_code != 200:
            raise credentials_exception

        user_data = response.json()

    return SUser(**user_data, token=token)
