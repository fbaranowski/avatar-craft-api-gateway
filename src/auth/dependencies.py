import aiohttp
import requests
import jwt
import json
from jwt import algorithms
from fastapi import HTTPException, Request
from settings import AuthSettings


async def get_current_user(request: Request):
    user = request.session.get('user')

    if not user:
        raise HTTPException(status_code=401, detail='Not authenticated')

    access_token = user.get('access_token', None)

    if not access_token:
        raise HTTPException(status_code=401, detail='Access token not found')

    header = jwt.get_unverified_header(access_token)

    async with aiohttp.ClientSession as session:
        async with session.get(f'https://{AuthSettings.AUTH0_DOMAIN}/.well-known/jwks.json') as response:
            if response.status != 200:
                raise HTTPException(status_code=500, detail='Failed to fetch JWKS')
            jwks = await response.json()

    public_key = None

    for jwk in jwks['keys']:
        if jwk['kid'] == header['kid']:
            public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))
            break

    if not public_key:
        raise Exception('Public key not found')

    try:
        payload = jwt.decode(
            access_token,
            public_key,
            algorithms=[AuthSettings.AUTH0_ALGORITHM],
            audience=AuthSettings.AUTH0_AUDIENCE,
            issuer=AuthSettings.AUTH0_ISSUER
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Token has expired')
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail='Invalid token')
