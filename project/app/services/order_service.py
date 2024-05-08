from .base_service import BaseService
from ..schemas.order_schema import OrderUpdate
from ..models import Order

"""Servicio base para el CRUD de ordenes en base de datos.
Args:
    model (Base): Modelo de base de datos a consular.
    update_model (Pydantic.BaseModel): Modelo de actualización de pydantic.
    get_all_join_attrs (list[str]): Lista de relaciones a traer en cada get_all.
    get_one_join_attrs (list[str]): Lista de relaciones a traer en cada get_one.
"""
OrderService = BaseService(
    model = Order,
    update_model = OrderUpdate,
    get_all_join_attrs = [],
    get_one_join_attrs = [],
    )
    