from pydantic import BaseModel
from typing import Union, Dict, List
from ..models import OrderStatus

class OrderUpdate(BaseModel):
    """Esquema de actualización completo de orden.

    Args:
        customer_id: (int|None). Identificador del cliente.
        business_id: (int|None). Identificador del negocio.
        lon: (float|None). Longitúd de la ubicación.
        lat: (float|None). Latitúd de de la ubicación.
        status: (str|None). Estado de la orden.
    """
    customer_id: Union[int, None] = None
    business_id: Union[int, None] = None
    lon: Union[float, None] = None
    lat: Union[float, None] = None
    status: Union[OrderStatus, None] = None

class RemoveProduct:
    """Esquema de remover producto a orden.

    Args:
        id: (int): Id del producto.
    """
    id: int