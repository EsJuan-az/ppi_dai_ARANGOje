
from .base_service import BaseService
from ..models import Order
from ..schemas.business_schema import BusinessUpdate

class OrderService(BaseService):
    """Servicio de Order: Maneja el CRUD de las ordenes en base 
    de datos.
    
    Args:
        model (SQLModel): Esquema o modelo de base de datos en SQL.
        update_model (Pydantic.BaseModel): Esquema para la actualización de entidad.
        get_all_join_attrs (list[str]): Relaciones a traer cada vez que se ejecuta un get_all.
        get_one_join_attrs (list[str]): Relaciones a traer cada vez que se ejecuta un get_one.
    """
    model = Order
    update_model = BusinessUpdate
    get_all_join_attrs = ['customer', 'products']
    get_one_join_attrs = ['customer', 'products']
    