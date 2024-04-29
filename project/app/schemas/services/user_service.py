from .base_login_service import LoginService
from ..models import User
from ..schemas.user_schema import UserUpdate

class UserService(LoginService):
    """Servicio de Usuario: Maneja el CRUD de los usuarios en base 
    de datos.
    
    Args:
        model (SQLModel): Esquema o modelo de base de datos en SQL.
        update_model (Pydantic.BaseModel): Esquema para la actualización de entidad.
        get_all_join_attrs (list[str]): Relaciones a traer cada vez que se ejecuta un get_all.
        get_one_join_attrs (list[str]): Relaciones a traer cada vez que se ejecuta un get_one.
    """
    model = User
    update_model = UserUpdate
    get_all_join_attrs = []
    get_one_join_attrs = []
    