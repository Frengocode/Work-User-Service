from fastapi import FastAPI
from src.user_service.router import user_router
from src.auth_service.router import auth_service
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="User Service")



app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://192.168.100.59:8000"],  # Разрешённые источники
    allow_credentials=True,
    allow_methods=["*"],  # Разрешённые методы (GET, POST и т.д.)
    allow_headers=["*"],  # Разрешённые заголовки
)


app.include_router(user_router)
app.include_router(auth_service)
