from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse

from auth.core import create_user
from auth.dependencies import get_user_payload
from auth.settings import AuthSettings

router = APIRouter()
oauth = OAuth()

oauth.register(
    name="auth0",
    client_id=AuthSettings.AUTH0_CLIENT_ID,
    client_secret=AuthSettings.AUTH0_CLIENT_SECRET,
    server_metadata_url=f"https://{AuthSettings.AUTH0_DOMAIN}/.well-known/openid-configuration",
    client_kwargs={"scope": "openid profile email"},
)


@router.get("/login")
async def login(request: Request):
    return await oauth.auth0.authorize_redirect(
        request, "http://localhost:8000/callback", audience=AuthSettings.AUTH0_AUDIENCE
    )


@router.get("/callback")
async def callback(request: Request):
    token = await oauth.auth0.authorize_access_token(request)

    request.session["access_token"] = token["access_token"]

    userinfo = token["userinfo"]
    email = userinfo["email"]

    await create_user(email)

    return RedirectResponse(url="/private")


@router.get("/logout")
async def logout(request: Request):
    request.session.clear()

    return RedirectResponse(
        url=f"https://{AuthSettings.AUTH0_DOMAIN}/v2/logout?"
        f"client_id={AuthSettings.AUTH0_CLIENT_ID}&"
        f"returnTo=http://localhost:8000/"
    )


@router.get("/")
async def public():
    return {
        "message": "Hello, this is AvatarCraft - application for creating avatars using AI"
    }


@router.get("/private")
async def profile(user_payload: dict = Depends(get_user_payload)):
    return {"message": "This is your private endpoint", "user_info": user_payload}
