import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_EXPIRATION = int(os.getenv("JWT_EXPIRATION", 3600))