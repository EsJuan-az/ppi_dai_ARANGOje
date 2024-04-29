from pydantic import BaseModel, ValidationError
from typing import Annotated, List, Union
class Login(BaseModel):
    """Esquema para el inicio de sesión de usuarios.

    Args:
        email (str): Email del usuario.
        password (str): Contraseña del usuario.
        scopes (list[str]): Lista de permisos requeridos.
        grant_type (str|None): Tipo de Inicio, Aceptado|Denegado.
        client_id: Identificador del usuario.
        client_secret: Llave de decodificación del Token.
    """
    email: str
    password: str
    scopes: list[str] = []
    grant_type: Union[str, None] = None
    client_id: Union[str, None] = None
    client_secret: Union[str, None] = None
    class Config:
        orm_mode = True