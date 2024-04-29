from .base_service import BaseService
from ..models import Business
from ..schemas.business_schema import BusinessUpdate

class BusinessService(BaseService):
    model = Business
    update_model = BusinessUpdate
    get_all_join_attrs = ['holder']
    get_one_join_attrs = []
    