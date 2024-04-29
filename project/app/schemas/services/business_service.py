from .base_service import BaseService
from ..models import Business
from ..schemas.business_schema import BusinessUpdate

class BusinessService(BaseService):
    """Servicio de Negocio: Maneja el CRUD de los negocios en base 
    de datos.
    
    Args:
        model (SQLModel): Esquema o modelo de base de datos en SQL.
        update_model (Pydantic.BaseModel): Esquema para la actualización de entidad.
        get_all_join_attrs (list[str]): Relaciones a traer cada vez que se ejecuta un get_all.
        get_one_join_attrs (list[str]): Relaciones a traer cada vez que se ejecuta un get_one.
    """
    model = Business
    update_model = BusinessUpdate
    get_all_join_attrs = ['holder']
    get_one_join_attrs = []
    