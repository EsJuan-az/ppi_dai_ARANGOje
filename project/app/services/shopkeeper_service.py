from .base_service import BaseService
from ..models import Shopkeeper
from ..schemas.shopkeeper_schema import ShopkeeperUpdate

class ShopkeeperService(BaseService):
    model = Shopkeeper
    update_model = ShopkeeperUpdate
    get_all_join_attrs = ['user', 'business']
    get_one_join_attrs = []