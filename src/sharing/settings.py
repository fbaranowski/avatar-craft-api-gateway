import os


class SharingSettings:
    CRUD_URL = os.getenv("GRAPHQL_API_URL")
    SHARING_URL = os.getenv("SHARING_URL")
