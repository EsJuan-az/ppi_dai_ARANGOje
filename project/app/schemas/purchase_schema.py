from pydantic import BaseModel
from typing import Union

class PurchaseUpdate(BaseModel):
    """Modelo completo de compra.

    Args:
        business_id: int. Identificador del negocio.
        customer_id: int|None. Identificador del cliente.
    """
    business_id: Union[int, None] = None
    customer_id: Union[int, None] = None
