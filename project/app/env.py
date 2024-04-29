import os
# En este archivo obtengo todas las variables de entorno.
DATABASE_URL = os.environ.get("DATABASE_URL") or '' # URL de conexión a la base de datos.
SECRET_KEY = os.environ.get('SECRET_KEY') or ''  # Llave privada de cifrado para el JWT.
ALGORITHM = os.environ.get('ALGORITHM') or 'HS256' # Algoritmo de cifrado de contraseñas.
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES') or "30") # Tiempo de expiración del token.
