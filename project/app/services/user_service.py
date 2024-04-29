from .base_login_service import LoginService
from ..models import User
from ..schemas.user_schema import UserUpdate

class UserService(LoginService):
    """Servicio base para el CRUD de usuarios en base de datos.
    Args:
        model (Base): Modelo de base de datos a consular.
        update_model (Pydantic.BaseModel): Modelo de actualización de pydantic.
        get_all_join_attrs (list[str]): Lista de relaciones a traer en cada get_all.
        get_one_join_attrs (list[str]): Lista de relaciones a traer en cada get_one.
    """
    model = User
    update_model = UserUpdate
    get_all_join_attrs = []
    get_one_join_attrs = []
    