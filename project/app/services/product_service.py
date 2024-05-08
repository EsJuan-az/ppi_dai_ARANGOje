from .base_service import BaseService
from ..models import Product
from ..schemas.product_schema import ProductUpdate

"""Servicio base para el CRUD de productos en base de datos.
Args:
    model (Base): Modelo de base de datos a consular.
    update_model (Pydantic.BaseModel): Modelo de actualización de pydantic.
    get_all_join_attrs (list[str]): Lista de relaciones a traer en cada get_all.
    get_one_join_attrs (list[str]): Lista de relaciones a traer en cada get_one.
"""
ProductService = BaseService(
    model = Product,
    update_model = ProductUpdate,
    get_all_join_attrs = ['business'],
    get_one_join_attrs = [],
    )