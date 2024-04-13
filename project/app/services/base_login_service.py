from ..models import Base
from ..services.base_service import BaseService 
from ..schemas.login_schema import Login
from sqlmodel import select, update, Session



class LoginService(BaseService):
    model = Base
    get_one_join_attrs = []
    @classmethod
    async def login(cls, session:Session, login:Login) -> model:
        stmt = select(cls.model)
        for joinAttr in cls.get_one_join_attrs:
            attr = getattr(cls.model, joinAttr)
            stmt = stmt.join(attr)
        stmt = stmt.where(cls.model.active)\
            .where(cls.model.email == login.email)\
            .where(cls.model.password == login.password)
        result = await session.exec(stmt)
        return result.one() 
