from fastapi  import Depends, HTTPException, security, APIRouter
from src.uitils.uitils import Uitils
import httpx
import asyncio

auth_service = APIRouter(tags=["Auth Service"])


@auth_service.post("/auth-login/", response_model=dict)
async def login(request: security.OAuth2PasswordRequestForm = Depends()):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://192.168.100.59:8000/user-service/api/v1/get-user-for-login/{request.username}/{request.password}/")

    if response.status_code == 200:
        user_data = response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Invalid credentials or external service error")

    access_token =  Uitils.create_access_token(data={"sub": user_data.get("username")})

    return {"access_token": access_token, "token_type": "bearer"}
