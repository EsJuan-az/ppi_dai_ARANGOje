from .base_service import BaseService
from ..models import Product
from ..schemas.product_schema import ProductUpdate

class ProductService(BaseService):
    """Servicio de Productos: Maneja el CRUD de los productos en base 
    de datos.
    
    Args:
        model (SQLModel): Esquema o modelo de base de datos en SQL.
        update_model (Pydantic.BaseModel): Esquema para la actualización de entidad.
        get_all_join_attrs (list[str]): Relaciones a traer cada vez que se ejecuta un get_all.
        get_one_join_attrs (list[str]): Relaciones a traer cada vez que se ejecuta un get_one.
    """
    model = Product
    update_model = ProductUpdate
    get_all_join_attrs = ['business']
    get_one_join_attrs = []