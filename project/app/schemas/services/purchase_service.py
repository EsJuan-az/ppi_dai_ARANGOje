from .base_service import BaseService
from ..models import Purchase
from ..schemas.business_schema import BusinessUpdate

class PurchaseService(BaseService):
    """Servicio de Negocio: Maneja el CRUD de los compras en base 
    de datos.
    
    Args:
        model (SQLModel): Esquema o modelo de base de datos en SQL.
        update_model (Pydantic.BaseModel): Esquema para la actualización de entidad.
        get_all_join_attrs (list[str]): Relaciones a traer cada vez que se ejecuta un get_all.
        get_one_join_attrs (list[str]): Relaciones a traer cada vez que se ejecuta un get_one.
    """
    model = Purchase
    update_model = BusinessUpdate
    get_all_join_attrs = ['customer', 'products']
    get_one_join_attrs = ['customer', 'products']
    