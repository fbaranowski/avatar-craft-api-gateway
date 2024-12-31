from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport

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

    request.session["user"] = token
    userinfo = token["userinfo"]
    email = str(userinfo["email"])

    transport = AIOHTTPTransport(url=AuthSettings.GRAPHQL_API_URL)

    async with Client(transport=transport, fetch_schema_from_transport=False) as client:
        query = gql(
            """
            mutation ($email: String!) {
                createUser(email: $email) {
                    id
                    mail
                }
            }
            """
        )
        variables = {"email": email}
        try:
            await client.execute(query, variable_values=variables)
        except Exception as e:
            print(f"error {e}")

    return RedirectResponse(url="/profile")


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


@router.get("/profile")
async def profile(request: Request):
    user = request.session.get("user")
    userinfo = user["userinfo"]
    email = userinfo["email"]

    if not user:
        raise HTTPException(
            status_code=401,
            detail="You are not authorized to see this page, please log in",
        )

    return {"message": "This is your private endpoint", "user": user, "mail": email}
