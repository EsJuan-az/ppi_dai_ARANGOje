from pydantic import BaseModel
from typing import Union

class OrderProductUpdate(BaseModel):
    """Esquema de actualización de relación orden-producto.

    Args:
        order_id: (int|None). Identificador de orden.
        product_id: (int|None). Identificador del producto.
        amount: (int|None). Cantidad del producto.
    """
    order_id: Union[int, None] = None
    product_id: Union[int, None] = None
    amount: Union[int, None] = None
    class Config:
        # Ésta configuración está destinada a una mejor
        # interacción con la base de datos.
        orm_mode = True
    