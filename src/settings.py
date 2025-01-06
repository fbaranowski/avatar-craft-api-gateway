import os


class AppSettings:
    SECRET_KEY = os.getenv("SECRET_KEY")
