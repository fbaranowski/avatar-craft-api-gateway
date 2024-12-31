import os

from dotenv import find_dotenv, load_dotenv

find_dotenv()

load_dotenv()


class AppSettings:
    SECRET_KEY = os.getenv("SECRET_KEY")
