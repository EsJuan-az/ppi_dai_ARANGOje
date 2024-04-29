from .base_service import BaseService
from ..models import OrderProduct
from ..schemas.business_schema import BusinessUpdate

class OrderProductService(BaseService):
    """Servicio de OrderProduct: Maneja el CRUD de las relaciones en base 
    de datos.
    
    Args:
        model (SQLModel): Esquema o modelo de base de datos en SQL.
        update_model (Pydantic.BaseModel): Esquema para la actualización de entidad.
        get_all_join_attrs (list[str]): Relaciones a traer cada vez que se ejecuta un get_all.
        get_one_join_attrs (list[str]): Relaciones a traer cada vez que se ejecuta un get_one.
    """
    model = OrderProduct
    update_model = BusinessUpdate
    get_all_join_attrs = ['product', 'order']
    get_one_join_attrs = ['product', 'order']
    