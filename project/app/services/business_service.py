from .base_service import BaseService
from ..models import Business
from ..schemas.business_schema import BusinessUpdate

"""Servicio base para el CRUD de negocios en base de datos.
Args:
    model (Base): Modelo de base de datos a consular.
    update_model (Pydantic.BaseModel): Modelo de actualización de pydantic.
    get_all_join_attrs (list[str]): Lista de relaciones a traer en cada get_all.
    get_one_join_attrs (list[str]): Lista de relaciones a traer en cada get_one.
"""
BusinessService = BaseService(
    model = Business,
    update_model = BusinessUpdate,
    get_all_join_attrs = ['holder'],
    get_one_join_attrs = ['holder'],
)