import os
from dotenv import load_dotenv
# En este archivo obtengo todas las variables de entorno.
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", '') # URL de conexión a la base de datos.
SECRET_KEY = os.getenv('SECRET_KEY', '')  # Llave privada de cifrado para el JWT.
ALGORITHM = os.getenv('ALGORITHM', 'HS256')  # Algoritmo de cifrado de contraseñas.
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 180)) # Tiempo de expiración del token.
PORT = int(os.getenv('PORT', 8000))