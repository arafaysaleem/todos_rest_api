import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    ENV:str = os.getenv('FLASK_ENV', default='')
    DEBUG:bool = bool(os.getenv('FLASK_DEBUG', default=False))
    PORT:int = int(os.getenv('PORT', default=5000))
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', default='super-secret-key')
    JWT_EXPIRATION_HOURS:int = int(os.getenv('JWT_EXPIRATION_HOURS', default=1))