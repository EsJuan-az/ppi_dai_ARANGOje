from .base_service import BaseService
from ..models import Product
from ..schemas.product_schema import ProductUpdate

class ProductService(BaseService):
    model = Product
    update_model = ProductUpdate
    get_all_join_attrs = ['business']
    get_one_join_attrs = []