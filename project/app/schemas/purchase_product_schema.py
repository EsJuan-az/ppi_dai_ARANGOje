from pydantic import BaseModel
from typing import Union
class PurchaseProductUpdate(BaseModel):
    """Esquema de actualización completo de relación compra-producto.

    Args:
        purchase_id: (int|None). Identificador de compra.
        product_id: (int|None). Identificador del producto.
        amount: (int|None). Cantidad del producto.
    """
    purchase_id: Union[int, None] = None
    product_id: Union[int, None] = None
    amount: Union[int, None] = None