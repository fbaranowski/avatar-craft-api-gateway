import aiohttp
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
# from auth.settings import AuthSettings
from settings import AuthSettings

router = APIRouter()
oauth = OAuth()

oauth.register(
    name='auth0',
    client_id=AuthSettings.AUTH0_CLIENT_ID,
    client_secret=AuthSettings.AUTH0_CLIENT_SECRET,
    server_metadata_url=f'https://{AuthSettings.AUTH0_DOMAIN}/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid profile email'}
)


@router.get('/login')
async def login(request: Request):
    return await oauth.auth0.authorize_redirect(
        request,
        'http://localhost:8000/callback',
        audience=AuthSettings.AUTH0_AUDIENCE
    )


@router.get('/callback')
async def callback(request: Request):
    token = await oauth.auth0.authorize_access_token(request)
    request.session['user'] = token
    userinfo = token['userinfo']
    # request.session['email'] = userinfo['email']
    print(type(userinfo['email']))
    email = str(userinfo['email'])
    transport = AIOHTTPTransport(url=AuthSettings.GRAPHQL_API_URL)
    # graphql_url = 'http://localhost:8100/graphql'
    async with Client(transport=transport, fetch_schema_from_transport=False) as client:
        query = gql("""
            mutation ($email: String!) {
                createUser(email: $email) {
                    id
                    mail
                }
            }
            """)
        variables = {'email': email}
        try:
            response = await client.execute(query, variable_values=variables)
            print('created user')
        except Exception as e:
            print(f'error {e}')
    # async with aiohttp.ClientSession() as session:
    #     await session.post(AppSettings.GRAPHQL_API_URL, json={'query': query, 'variables': variables})

    return RedirectResponse(url='/private')


@router.get('/logout')
async def logout(request: Request):
    request.session.clear()

    return RedirectResponse(
        url=f'https://{AuthSettings.AUTH0_DOMAIN}/v2/logout?'
            f'client_id={AuthSettings.AUTH0_CLIENT_ID}&'
            f'returnTo=http://localhost:8000/public'
    )


@router.get('/public')
async def public(request: Request):
    return {'message': 'This is public endpoint'}


@router.get('/private')
async def profile(request: Request):
    user = request.session.get('user')
    userinfo = user['userinfo']
    email = userinfo['email']

    if not user:
        raise HTTPException(status_code=401, detail='You are not authorized to see this page, please log in')

    return {'message': 'This is private endpoint', 'user': user, 'mail': email}
