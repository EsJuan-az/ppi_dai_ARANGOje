from ..models import Base
from ..services.base_service import BaseService 
from ..schemas.login_schema import Login
from sqlmodel import select, update, Session



class LoginService(BaseService):
    """Servicio base para el CRUD + Login de entidades en base de datos.
    Args:
        model (Base): Modelo de base de datos a consular.
        get_one_join_attrs (list[str]): Lista de relaciones a traer en cada get_one.
    """
    async def login(self, session:Session, login:Login):
        """Login: dado un email y password, regresa entidad.

        Args:
            session (Session): Sesión de base de datos.
            login (Login): Objeto con datos de login.

        Returns:
            model: Objeto que cumple la condición.
        """
        stmt = select(self.model)
        for joinAttr in self.get_one_join_attrs:
            attr = getattr(self.model, joinAttr)
            stmt = stmt.join(attr)
        stmt = stmt.where(self.model.email == login.email)\
            .where(self.model.password == login.password)
        result = await session.exec(stmt)
        return result.one() 
    
    
    async def get_by_email(self, session:Session, email:str):
        """Get by email: dado un email, regresa entidad.
        Args:
            session (Session): Sesión de base de datos.
            email(str): email para obtener.
        Returns:
            model: Objeto que cumple la condición.
        """
        stmt = select(self.model)
        for joinAttr in self.get_one_join_attrs:
            attr = getattr(self.model, joinAttr)
            stmt = stmt.join(attr)
        stmt = stmt.where(self.model.email == email)
        result = await session.exec(stmt)
        return result.one() 
