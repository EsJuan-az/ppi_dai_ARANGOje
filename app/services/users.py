from ..models import User
from ..schemas import UserCreate, UserUpdate
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, update

class UserService:
    @staticmethod
    def get_all(session:Session, offset:int, limit:int):
        stmt = select(User).where(User.active).offset(offset).limit(limit)
        return session.scalars(stmt).all()
    
    @staticmethod
    def get_by_id(session:Session, id:int):
        stmt = select(User).where(User.active).where(User.id == id)
        return session.scalars(stmt).first()
    
    @staticmethod
    def login(session:Session, email:str, password:str):
        stmt = select(User).where(User.active).where(User.email == email).where(User.password == password)
        return session.scalars(stmt).first()
    
    @staticmethod
    def create(session:Session, user:UserCreate):
        stmt = insert(User).values(**user.dict()).returning(User)
        with session.execute(stmt) as result:
            session.commit()
            return result.first()
        
    @staticmethod
    def update(session:Session, user:UserUpdate):
        stmt = update(User).where(User.active).where(User.id == user.id).values(**user.dict()).returning(User)
        with session.execute(stmt) as result:
            session.commit()
            return result.scalar_one()
    
    @staticmethod
    def delete(session:Session, id: int):
        stmt = update(User).where(User.active).where(User.id == id).values(active = False).returning(User)
        with session.execute(stmt) as result:
            session.commit()
            return result.scalar_one()