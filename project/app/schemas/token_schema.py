from pydantic import BaseModel, ValidationError
from typing import Annotated, List, Union

class Token(BaseModel):
    """Esquema de retorno del token:

    Args:
        access_token (str): JWT generado.
        token_type (str): Tipo del token retornado.
    """
    access_token: str
    token_type: str
    
    
class TokenData(BaseModel):
    """Esquema de generación del token:

    Args:
        id (str|None): Identificador del usuario.
        scopes (list[str]): Permisos del usuario.
    """
    id: Union[int, None] = None
    scopes: List[str] = []


