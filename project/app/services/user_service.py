from .base_login_service import LoginService
from ..models import User
from ..schemas.user_schema import UserUpdate

class UserService(LoginService):
    model = User
    update_model = UserUpdate
    get_all_join_attrs = []
    get_one_join_attrs = []
    