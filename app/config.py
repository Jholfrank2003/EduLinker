import os
from dotenv import load_dotenv

# Cargar variables desde .env
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "clave-super-secreta")
    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_USER = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
    MYSQL_DB = os.getenv("MYSQL_DB", "Edulinker")
    MYSQL_CURSORCLASS = 'DictCursor'
