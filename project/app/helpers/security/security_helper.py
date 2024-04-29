# LIBRERÍAS EXTERNAS.
from datetime import datetime, timedelta, timezone
from typing import Annotated, Union
from sqlmodel import Session
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import (
    OAuth2PasswordBearer,
    SecurityScopes,
)
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import ValidationError
# MODULOS.
from ...database import get_db
from ...env import ALGORITHM, SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES
from ...schemas.token_schema import TokenData, Token
from ...schemas.login_schema import Login
from ...services.user_service import UserService
# Aquí creamos un contexto de encriptación.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# Creamos un esquema de autenticación.
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={"me": "Read information about the current user.", "items": "Read items."},
)

class UserSecurityHelper:
    """User Security Helper: Funciones de seguridad general para la clase usuario
    como lo son cifrar y comparar contraseñas, etcétera.
    """
    @staticmethod
    def verify_password(plain_password, hashed_password):
        """Verifica si la contraseña es o no valida.
        Args:
            plain_password (str): Contraseña plana de pregunta.
            hashed_password (str): Hash de la contraseña en base de datos.
        Returns:
            bool: si la contraseña es o no válida.
        """
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        """Encripta una contraseña en texto plano dada.
        Args:
            password (str): Contraseña a encriptar.
        Returns:
            str: Hash de la contraseña para almacenar en base.
        """
        return pwd_context.hash(password)

    @staticmethod
    async def authenticate(db, login: Login):
        """Dado un email y password, verifica las credenciales.

        Args:
            db (Session): Motor de base de datos.
            email (str): Email de entidad.
            password (str): Password de entidad

        Returns:
            dict: Entidad.
        """
        user = await UserService.get_by_email(db, login.email)
        if not user:
            return False
        if not UserSecurityHelper.verify_password(login.password, user.password):
            return False
        data = { "sub": user.id }
        jwt = UserSecurityHelper.create_access_token(data)
        return Token(access_token=jwt, token_type='bearer')

    @staticmethod
    def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
        """Dados unos credenciales, genera el token de acceso
        Args:
            data (dict): Credenciales.
            expires_delta (Union[timedelta, None], optional): Tiempo en minutos de expiración. Defaults to None.
        Returns:
            str: JWT de autenticación.
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    async def get_current(
        security_scopes: SecurityScopes,
        token: Annotated[str, Depends(oauth2_scheme)],
        session: Annotated[Session, Depends(get_db)]
    ):
        """Dado un token, obtiene el usuario correspondiente.
        Args:
            security_scopes (SecurityScopes): _description_
            token (Annotated[str, Depends): Token a parsear.
            session (Annotated[Session, Depends): Sesión de base de datos.
        Raises:
            credentials_exception: Posible error de credenciales.
            HTTPException: Desencadena error de protocolo.
        Returns:
            dict: Datos del usuario.
        """
        # Añadimos los scopes al token en caso de existir.
        if security_scopes.scopes:
            authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
        else:
            authenticate_value = "Bearer"
            
        # Declaramos una excepción en caso de necesitarla.    
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales invalidas",
            headers={"WWW-Authenticate": authenticate_value},
        )
        token_data = None
        
        # Aquí decodificamos el JWT.
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={'verify_sub': False})
            id: int = payload.get("sub")
            if id is None:
                raise credentials_exception
            token_scopes = payload.get("scopes", [])
            token_data = TokenData(scopes=token_scopes, id=id)
        except (JWTError, ValidationError):
            print(credentials_exception)
            raise credentials_exception
        
        #Verificamos que existe la token data.
        if token_data is None or token_data.id is None:
            raise credentials_exception
        
        # Obtenemos el usuario.
        user = await UserService.get_by_id(session, id=token_data.id)
        if user is None:
            raise credentials_exception
        # Verifica las autorizaciones, y en caso de no tener las requeridas regresa error.
        for scope in security_scopes.scopes:
            if scope not in token_data.scopes:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="No se tienen permisos para ésta acción",
                    headers={"WWW-Authenticate": authenticate_value},
                )
        return user
