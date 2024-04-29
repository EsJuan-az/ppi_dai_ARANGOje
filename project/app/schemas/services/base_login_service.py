from ..models import Base
from ..services.base_service import BaseService 
from ..schemas.login_schema import Login
from sqlmodel import select, update, Session



class LoginService(BaseService):
    """LoginService: Este servicio maneja acciones como el login y la obtención
    según email además de las básicas del BaseService.
    
    Args:
        model (SQLModel): Esquema y modelo de datos SQLModel.
        get_one_join_attrs (list[str]): Relaciones que se van a traer con cada get_one.

    Extends:
        BaseService: Servicio de funcionalidades básicas.
    """
    model = Base
    get_one_join_attrs = []
    @classmethod
    async def login(cls, session:Session, login:Login) -> model:
        """Login: dado un email y password, regresa entidad.

        Args:
            session (Session): Sesión de base de datos.
            login (Login): Objeto con datos de login.

        Returns:
            model: Objeto que cumple la condición.
        """
        stmt = select(cls.model)
        for joinAttr in cls.get_one_join_attrs:
            attr = getattr(cls.model, joinAttr)
            stmt = stmt.join(attr)
        stmt = stmt.where(cls.model.active)\
            .where(cls.model.email == login.email)\
            .where(cls.model.password == login.password)
        result = await session.exec(stmt)
        return result.one() 
    @classmethod
    async def get_by_email(cls, session:Session, email:str) -> model:
        """Get by email: dado un email, regresa entidad.
        Args:
            session (Session): Sesión de base de datos.
            email(str): email para obtener.
        Returns:
            model: Objeto que cumple la condición.
        """
        stmt = select(cls.model)
        for joinAttr in cls.get_one_join_attrs:
            attr = getattr(cls.model, joinAttr)
            stmt = stmt.join(attr)
        stmt = stmt.where(cls.model.active)\
            .where(cls.model.email == email)
        result = await session.exec(stmt)
        return result.one() 
