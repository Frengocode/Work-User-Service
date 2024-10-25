from fastapi import HTTPException, Form, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from src.user_service.models import User
from src.schemes.user import UserResponse
from sqlalchemy import select
import httpx
from src.uitils.uitils import Uitils, Hash
from src.uitils.scheme import SUser
import logging
from src.schemes.user import UserResponse, SelectRole, VacancyResponse
from src.config.email import conf
from fastapi_mail import FastMail, MessageSchema
import uuid



log = logging.getLogger(__name__)

log.setLevel(logging.DEBUG)


class UserService:

    def __init__(self, session: AsyncSession, response: UserResponse, user_obj_: User, current_user: SUser = None):
        self.session = session
        self.response = response
        self.user_obj_ = user_obj_
        self.current_user = current_user 


    async def sign_up(
        self,
        role: SelectRole,
        username: str = Form(...),
        password: str = Form(...),
        email: str = Form(...),
        name: str = Form(...),
        surname: str = Form(...),
        age: int = Form(...)
    ):

        exist_username_query = await self.session.execute(
            select(User).filter_by(username=username, email=email)
        )

        exist_username = exist_username_query.scalars().first()
        if exist_username:
            log.warn("Error From user")
            raise HTTPException(
                detail="Username or email all ready used", status_code=403
            )

        ##### Hahsing Password
        hashed_password = Hash.bcrypt(password)
        log.info("Hashing User Password")

        if not email.endswith("@gmail.com"):
            log.error("Email Error")
            raise HTTPException(detail="Email Error", status_code=402)
        
        if len(username) < 5:
            raise HTTPException(detail="Username Error", status_code=402)

        user = self.user_obj_(username=username, password=hashed_password, email=email, name = name, surname = surname, role = role, age = age, picture_url = "https://repository-images.githubusercontent.com/15949540/b0a70b80-cb15-11e9-8338-661f601406a1", password_reset_tok = str(uuid.uuid4()))

        self.session.add(user)
        await self.session.commit()

        log.info("User Saved Succsesfully")


    async def get_user_for_login(self, username: str = Form(...), password: str = Form(...)):
        
        user_query = await self.session.execute(

            select(User)
            .filter_by(username = username)

        )

        user = user_query.scalars().first()
        if not user:
            raise HTTPException(detail= "User Not Found", status_code=404)
        
        if not Hash.verify(hashed_password=user.password, plain_password=password):
            raise HTTPException(detail=f"Password Error {password}", status_code=403)
        
        response = self.response(

            id = user.id,
            username = user.username,
            joined_at = user.joined_at,
            name = user.name,
            surname = user.surname,
            role = user.role,
            email = user.email,
            picture_url = user.picture_url,
            age = user.age,


        )

        return response



    async def get_current_user_(self, username: str):

        user_query = await self.session.execute(

            select(User)
            .filter(User.username == username)

        )

        user = user_query.scalars().first()
        if not user:
            raise HTTPException(
                detail="Not Found",
                status_code=404
            )
        
        response =  UserResponse(

            id = user.id,
            username = user.username,
            age = user.age,
            joined_at = user.joined_at,
            surname = user.surname,
            name = user.name,
            role = user.role,
            picture_url = user.picture_url,
            email = user.email,
            password = user.password


        )

        return response

    
    async def get_user_by_id(self, user_id: int, current_user: SUser):


        user_query = await self.session.execute(
            
            select(User)
            .filter(User.id == user_id)

        )



        user = user_query.scalars().first()
        if not user:
            log.error("User Not Found")
            raise HTTPException(
                detail="Not Found",
                status_code=404
            )


        
        response = UserResponse(

            id = user.id,
            username = user.username,
            age = user.age,
            surname = user.surname,
            name = user.name,
            company_name = user.company_name,
            email = user.email,
            role = user.role,
            picture_url = user.picture_url,
            joined_at = user.joined_at,
        )

        return response


    async def send_token_on_email(self, email: str):

        user_query = await self.session.execute(

            select(User)
            .filter(User.email == email)

        )

        user = user_query.scalars().first()
        if not user:
            raise HTTPException(
                detail=f"User With Email {email} Not Found",
                status_code=404
            )
        

        message = MessageSchema(
            subject="Token Request",
            recipients=[user.email],
            body=f"Please save This is Token In Good Place For not lost token http://192.168.100.59:8000/user-service/api/v1/password-resed-confirium/{user.password_reset_tok}/",
            subtype="plain"
        )
    
        fm = FastMail(conf)
        await fm.send_message(message)

        
        return {"detail": f"We Sended Token On This gmail {email}"}
    

    async def user_password_resed_confirium(self, token: str, old_password: str, new_password: str):
        
        user_query = await self.session.execute(

            select(User)
            .filter(User.password_reset_tok == token)
        )

        user = user_query.scalars().first()
        if not user:
            raise HTTPException(
                detail="User Not Found",
                status_code=404
            )

        if not Hash.verify(hashed_password=user.password, plain_password=old_password):
            raise HTTPException(detail=f"Password Error {old_password}", status_code=403)
        

        user.password = Hash.bcrypt(new_password)

        await self.session.commit()

        return {"Detail": "Your Password Changed succsesfully"}
    

    async def delete_user(self, user_id: int):
        
        user_query = await self.session.execute(

            select(User)
            .filter(User.id == user_id)

        )

        user = user_query.scalars().first()
        if not user:
            raise HTTPException(
                detail="Not Found",
                status_code=404
            )
        

        await self.session.delete(user)
        await self.session.commit()
        
        return "Deleted Succsesfully"