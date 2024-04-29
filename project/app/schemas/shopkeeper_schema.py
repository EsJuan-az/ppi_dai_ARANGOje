from pydantic import BaseModel
from typing import Union


class ShopkeeperUpdate(BaseModel):
    """Esquema de actualización de shopkeeper en 
    base de datos.
    
    Args:
        user_id (int|None): Identificador del usuario.
        business_id (int|None): Identificador del negocio.
    """
    business_id: Union[int, None] = None
    user_id: Union[int, None] = None
    lon: Union[float, None] = None
    lat: Union[float, None] = None
    working: Union[bool, None] = None
    class Config:
        orm_mode = True