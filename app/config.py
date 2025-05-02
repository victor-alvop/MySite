import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    #source database connection
    #DB_SOURCE_URL = os.getenv("DATABASE_SOURCE_URL")
    #target database connection
    #DB_TARGET_URL = os.getenv("DATABASE_TARGET_URL")

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_BINDS = {
        "DB_SOURCE_URL": os.getenv("DATABASE_SOURCE_URL"),
        "DB_TARGET_URL": os.getenv("DATABASE_TARGET_URL")
    }