from .base_service import BaseService
from ..models import Record

"""Servicio base para el CRUD de tenderos en base de datos.
Args:
    model (Base): Modelo de base de datos a consular.
    update_model (Pydantic.BaseModel): Modelo de actualización de pydantic.
    get_all_join_attrs (list[str]): Lista de relaciones a traer en cada get_all.
    get_one_join_attrs (list[str]): Lista de relaciones a traer en cada get_one.
"""
RecordService = BaseService(
    model = Record,
    get_all_join_attrs = ['user', 'business'],
    get_one_join_attrs = [],
    )