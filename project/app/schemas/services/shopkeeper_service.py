from .base_service import BaseService
from ..models import Shopkeeper
from ..schemas.shopkeeper_schema import ShopkeeperUpdate

class ShopkeeperService(BaseService):
    """Servicio de Shopkeeper: Maneja el CRUD de los shopkeepers en base 
    de datos.
    
    Args:
        model (SQLModel): Esquema o modelo de base de datos en SQL.
        update_model (Pydantic.BaseModel): Esquema para la actualización de entidad.
        get_all_join_attrs (list[str]): Relaciones a traer cada vez que se ejecuta un get_all.
        get_one_join_attrs (list[str]): Relaciones a traer cada vez que se ejecuta un get_one.
    """
    model = Shopkeeper
    update_model = ShopkeeperUpdate
    get_all_join_attrs = ['user', 'business']
    get_one_join_attrs = []