from ..models import User
from ..schemas import UserCreate, UserUpdate, Login
from sqlalchemy.orm import Session, contains_eager
from sqlalchemy import select, insert, update

class UserService:
    @staticmethod
    def get_all(session:Session, offset:int, limit:int):
        stmt = select(User)\
            .outerjoin(User.businesses)\
            .outerjoin(User.shopkeepers)\
            .where(User.active)\
            .offset(offset)\
            .limit(limit)\
            .options(contains_eager(User.businesses), contains_eager(User.shopkeepers))
        return session.scalars(stmt).unique().all()
    
    @staticmethod
    def get_by_id(session:Session, id:int):
        stmt = select(User)\
            .outerjoin(User.businesses)\
            .outerjoin(User.shopkeepers)\
            .where(User.active)\
            .where(User.id == id)\
            .options(contains_eager(User.businesses), contains_eager(User.shopkeepers))
        return session.scalars(stmt).unique().first()
    
    @staticmethod
    def login(session:Session, login:Login):
        stmt = select(User)\
            .outerjoin(User.businesses)\
            .outerjoin(User.shopkeepers)\
            .where(User.shopkeepers.active)\
            .where(User.businesses.active)\
            .where(User.active)\
            .where(User.email == login.email)\
            .where(User.password == login.password)\
            .options(contains_eager(User.businesses), contains_eager(User.shopkeepers))
        return  session.scalars(stmt).unique().first()

    @staticmethod
    def create(session:Session, user:UserCreate):
        user_dict = user.model_dump()
        for key, value in user_dict.copy().items():
            if value == None:
                del user_dict[key]
        stmt = insert(User).values(**user_dict).returning(User)
        with session.execute(stmt) as result:
            session.commit()
            return result.scalar_one()
        
    @staticmethod
    def update(session:Session, user:UserUpdate):
        user_dict = user.model_dump()
        for key, value in user_dict.copy().items():
            if value == None:
                del user_dict[key]
        stmt = update(User).where(User.active).where(User.id == user.id).values(**user_dict).returning(User)
        with session.execute(stmt) as result:
            session.commit()
            return result.scalar_one()
    
    @staticmethod
    def delete(session:Session, id: int):
        stmt = update(User).where(User.active).where(User.id == id).values(active = False).returning(User)
        with session.execute(stmt) as result:
            session.commit()
            return result.scalar_one()
        
        