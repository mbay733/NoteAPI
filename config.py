import os
from pathlib import Path

BASE_DIR = Path(__file__).parent


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI', f"sqlite:///{BASE_DIR / 'main.db'}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False  
    DEBUG = True
    PORT = 5000
    SECRET_KEY = "My secret key =)"