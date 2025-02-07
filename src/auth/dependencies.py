import json

import aiohttp
import jwt
from fastapi import Depends, Header
from jwt import algorithms

import auth.exceptions as exceptions
from auth.settings import AuthSettings


async def get_user_payload(authorization: str = Header(None)) -> dict:
    if not authorization or not authorization.startswith("Bearer "):
        raise exceptions.AccessTokenNotFoundException()

    access_token = authorization.split("Bearer ")[1]

    header = jwt.get_unverified_header(access_token)

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
            access_token,
            public_key,
            algorithms=[AuthSettings.AUTH0_ALGORITHM],
            audience=AuthSettings.AUTH0_AUDIENCE,
            issuer=AuthSettings.AUTH0_ISSUER,
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise exceptions.ExpiredTokenException()
    except jwt.InvalidTokenError:
        raise exceptions.InvalidTokenException()


async def get_current_user_email(user_payload: dict = Depends(get_user_payload)) -> str:
    namespace = AuthSettings.AUTH0_NAMESPACE
    email = user_payload.get(f"{namespace}/email")
    return email


def check_admin_role(user_payload: dict = Depends(get_user_payload)) -> bool:
    namespace = AuthSettings.AUTH0_NAMESPACE
    roles = user_payload.get(f"{namespace}/roles", [])

    if "admin" not in roles:
        return False

    return True
