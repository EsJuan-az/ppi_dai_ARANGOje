from .base_service import BaseService
from ..schemas.purchase_product_schema import PurchaseProductUpdate
from ..models import PurchaseProduct

class PurchaseService(BaseService):
    """Servicio base para el CRUD de relación compras-producto en base de datos.
    Args:
        model (Base): Modelo de base de datos a consular.
        update_model (Pydantic.BaseModel): Modelo de actualización de pydantic.
        get_all_join_attrs (list[str]): Lista de relaciones a traer en cada get_all.
        get_one_join_attrs (list[str]): Lista de relaciones a traer en cada get_one.
    """
    model = PurchaseProduct
    update_model = PurchaseProductUpdate
    get_all_join_attrs = ['purchase', 'product']
    get_one_join_attrs = ['purchase', 'product']
    