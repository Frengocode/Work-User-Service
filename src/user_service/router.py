from fastapi import APIRouter, Depends, Form
from src.uitils.uitils import Uitils
from src.service.api.v1.user_service import UserService, SelectRole, UserResponse, User
from sqlalchemy.ext.asyncio import AsyncSession
from src.config.database import get_user_session
from src.auth_service.oauth import get_current_user
from src.uitils.scheme import SUser


user_router = APIRouter(tags=["User"], prefix="/user-service/api/v1")


@user_router.post("/sing-up/")
async def create_account(
    role: SelectRole,
    session: AsyncSession = Depends(Uitils.get_user_session),
    email: str = Form(...),
    password: str = Form(...),
    username: str = Form(...),
    age: int = Form(...),
    name: str = Form(...),
    surname: str = Form(...)
):
    user_service = UserService(session=session, response=UserResponse, user_obj_=User)
    role_select = role.value
    return await user_service.sign_up(
        email=email, username=username, password=password, age=age, role=role_select, name = name, surname = surname
    )


@user_router.get("/get-user-for-login/{username}/{password}/", response_model=UserResponse)
async def get_user_for_auth_login(username: str, password: str, session: AsyncSession = Depends(get_user_session)):
    user_service = UserService(session=session, user_obj_=User, response=UserResponse)
    return await user_service.get_user_for_login(username=username, password=password)


@user_router.get("/get-current-user/{username}/", response_model=UserResponse)
async def get_user_with_username(username: str, session: AsyncSession = Depends(get_user_session)):
    service = UserService(session=session, user_obj_=User, response=UserResponse)
    return await service.get_current_user_(username=username)



@user_router.get("/get-user/{user_id}/", response_model=UserResponse)
async def get_user(user_id: int, session: AsyncSession = Depends(get_user_session), current_user: SUser = Depends(get_current_user)):
    serivce = UserService(session=session, user_obj_=User, response=UserResponse, current_user=current_user)
    return await serivce.get_user_by_id(user_id=user_id, current_user=current_user)


@user_router.post("/send-token-on-email/{gmail}")
async def send_token(gmail: str, session: AsyncSession = Depends(get_user_session)):
    sercice = UserService(session=session,  response=SUser, user_obj_=User)
    return await sercice.send_token_on_email(email=gmail)


@user_router.patch("/password-resed-confirium/{token}/")
async def update_password(token: str, new_password: str, old_password: str, session: AsyncSession = Depends(get_user_session)):
    service = UserService(session=session, user_obj_=User, response=UserResponse)
    return await service.user_password_resed_confirium(new_password = new_password, old_password=old_password, token=token)



@user_router.delete("/delete-user/{user_id}/")
async def delete_user_obj(user_id : int, session: AsyncSession = Depends(get_user_session)):
    service = UserService(session=session, response=SUser, user_obj_=User)
    return await service.delete_user(user_id=user_id)
