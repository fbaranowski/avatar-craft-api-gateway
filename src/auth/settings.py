import os

from dotenv import find_dotenv, load_dotenv

find_dotenv()

load_dotenv()


class AuthSettings:
    AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
    AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
    AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
    AUTH0_AUDIENCE = os.getenv("AUTH0_AUDIENCE")
    AUTH0_ISSUER = os.getenv("AUTH0_ISSUER")
    AUTH0_ALGORITHM = os.getenv("AUTH0_ALGORITHM")
    AUTH0_NAMESPACE = os.getenv("AUTH0_NAMESPACE")
    GRAPHQL_API_URL = os.getenv("GRAPHQL_API_URL")
