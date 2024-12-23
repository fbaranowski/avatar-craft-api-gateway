import os
from dotenv import find_dotenv, load_dotenv

find_dotenv()

load_dotenv()


class CrudSettings:
    GRAPHQL_API_URL = os.getenv("GRAPHQL_API_URL")
