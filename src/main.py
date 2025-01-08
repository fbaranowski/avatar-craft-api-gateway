from authlib.integrations.starlette_client import OAuth
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from auth.routers import router as auth_router
from crud.routers.avatars import router as avatars_router
from crud.routers.users import router as users_router
from settings import AppSettings

app = FastAPI()
oauth = OAuth()

app.add_middleware(
    middleware_class=SessionMiddleware, secret_key=f"{AppSettings.SECRET_KEY}"
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(avatars_router)
