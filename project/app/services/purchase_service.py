from .base_service import BaseService
from ..schemas.purchase_schema import PurchaseUpdate
from ..models import Purchase

class PurchaseService(BaseService):
    """Servicio base para el CRUD de compras en base de datos.
    Args:
        model (Base): Modelo de base de datos a consular.
        update_model (Pydantic.BaseModel): Modelo de actualización de pydantic.
        get_all_join_attrs (list[str]): Lista de relaciones a traer en cada get_all.
        get_one_join_attrs (list[str]): Lista de relaciones a traer en cada get_one.
    """
    model = Purchase
    update_model = PurchaseUpdate
    get_all_join_attrs = ['customer', 'business', 'products']
    get_one_join_attrs = ['customer', 'business', 'products']
    