import json

import aiohttp
import jwt
from fastapi import Depends, Request
from jwt import algorithms

import auth.exceptions as exceptions
from auth.settings import AuthSettings


async def get_user_payload(request: Request):
    id_token = request.session.get("id_token", None)

    if not id_token:
        raise exceptions.IDTokenNotFoundException()

    header = jwt.get_unverified_header(id_token)

    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"https://{AuthSettings.AUTH0_DOMAIN}/.well-known/jwks.json"
        ) as response:
            if response.status != 200:
                raise exceptions.JWKSFetchFailedException()
            jwks = await response.json()

    public_key = None

    for jwk in jwks["keys"]:
        if jwk["kid"] == header["kid"]:
            public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))
            break

    if not public_key:
        raise Exception("Public key not found")

    try:
        payload = jwt.decode(
            id_token,
            public_key,
            algorithms=[AuthSettings.AUTH0_ALGORITHM],
            audience=AuthSettings.AUTH0_CLIENT_ID,
            issuer=AuthSettings.AUTH0_ISSUER,
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise exceptions.ExpiredTokenException()
    except jwt.InvalidTokenError:
        raise exceptions.InvalidTokenException()


async def get_current_user_email(user_payload: dict = Depends(get_user_payload)):
    email = user_payload.get("email", None)
    return email


def check_admin_role(user_payload: dict = Depends(get_user_payload)):
    namespace = AuthSettings.AUTH0_NAMESPACE
    roles = user_payload.get(f"{namespace}/roles", [])

    if "admin" not in roles:
        return False

    return True
