from datetime import timedelta
from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    DEBUG = False
    # Usar puerto 5001 por defecto para evitar conflictos con Windows
    PORT = 5001
    HOST = '0.0.0.0'  # Permitir conexiones externas
    SQLALCHEMY_DATABASE_URI = "sqlite:///project.db"
    CORS_ORIGINS = ["http://localhost:3000"]
    JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']  # Cambia esto!
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

class DevConfig(Config):
    DEBUG = True
    HOST = 'localhost'  # Más seguro para desarrollo

class ProdConfig(Config):
    DEBUG = False
    # En producción, preferiblemente usar variables de entorno
    # para el puerto y host

config_selection = {
    "development": DevConfig(),
    "production": ProdConfig()
}