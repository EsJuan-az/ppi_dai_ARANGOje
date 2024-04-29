from .base_service import BaseService
from ..schemas.order_product_schema import OrderProductUpdate
from ..models import OrderProduct

class OrderProductService(BaseService):
    """Servicio base para el CRUD de relaciones order-product en base de datos.
    Args:
        model (Base): Modelo de base de datos a consular.
        update_model (Pydantic.BaseModel): Modelo de actualización de pydantic.
        get_all_join_attrs (list[str]): Lista de relaciones a traer en cada get_all.
        get_one_join_attrs (list[str]): Lista de relaciones a traer en cada get_one.
    """
    model = OrderProduct
    update_model = OrderProductUpdate
    get_all_join_attrs = ['product', 'order']
    get_one_join_attrs = ['product', 'order']
    