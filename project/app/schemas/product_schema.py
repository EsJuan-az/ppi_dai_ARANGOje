from pydantic import BaseModel
from typing import Union, List


class ProductUpdate(BaseModel):
    """Esquema de actualización de productos en 
    base de datos.
    
    Args:
        name (str|None): Nombre del usuario.
        description (str|None): Descripción del producto.
        price (float|None): Precio del producto.
        stock (int|None): Existencias del producto.
        business_id (int|None): Identificador del negocio.
    """
    name: Union[str, None] = None
    description: Union[str, None] = None
    price: Union[float, None] = None
    stock: Union[int, None] = None
    business_id: Union[int, None] = None
    images: Union[List[str], None] = None
    class Config:
        orm_mode = True