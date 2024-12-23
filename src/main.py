from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth
from auth.routers import router as auth_router
from settings import AppSettings
from crud.routers import router as crud_router


app = FastAPI()
oauth = OAuth()

app.add_middleware(middleware_class=SessionMiddleware, secret_key=f'{AppSettings.SECRET_KEY}')

app.include_router(auth_router)
app.include_router(crud_router)
