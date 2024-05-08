from .base_service import BaseService
from ..models import Shopkeeper
from ..schemas.shopkeeper_schema import ShopkeeperUpdate

"""Servicio base para el CRUD de tenderos en base de datos.
Args:
    model (Base): Modelo de base de datos a consular.
    update_model (Pydantic.BaseModel): Modelo de actualización de pydantic.
    get_all_join_attrs (list[str]): Lista de relaciones a traer en cada get_all.
    get_one_join_attrs (list[str]): Lista de relaciones a traer en cada get_one.
"""
ShopkeeperService = BaseService(
    model = Shopkeeper,
    update_model = ShopkeeperUpdate,
    get_all_join_attrs = ['user', 'business'],
    get_one_join_attrs = [],
    )