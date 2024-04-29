from pydantic import BaseModel
from datetime import datetime
from typing import Union

class BusinessUpdate(BaseModel):
    """Esquema de actualización de negocios en 
    base de datos.
    
    Args:
        name (str|None): Nombre del usuario.
        holder_id (int|None): Identificador del propietario del negocio.
    """
    name: Union[str, None] = None
    holder_id: Union[int, None] = None
    description: Union[str, None] = None
    image: Union[str, None] = None
    class Config:
        orm_mode = True