import os
DATABASE_URL = os.environ.get("DATABASE_URL") or ''
SECRET_KEY = os.environ.get('SECRET_KEY') or '' 
ALGORITHM = os.environ.get('ALGORITHM') or 'HS256' 
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES') or "30")
