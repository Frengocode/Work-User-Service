from fastapi import FastAPI
from src.user_service.router import user_router
from src.auth_service.router import auth_service
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="User Service")



app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://your_host:8000"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)


app.include_router(user_router)
app.include_router(auth_service)
