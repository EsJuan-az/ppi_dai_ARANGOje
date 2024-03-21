from ..models import Business, User
from ..schemas import BusinessCreate, BusinessUpdate, Login
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, insert, update



class BusinessService:
    @staticmethod
    def get_all(session:Session, offset:int, limit:int):
        stmt = select(Business)\
            .join(Business.holder)\
            .where(Business.active)\
            .offset(offset)\
            .limit(limit)\
            .options(joinedload(Business.holder))
        result = session.scalars(stmt).all()
        return result
    
    @staticmethod
    def get_by_id(session:Session, id:int):
        stmt = select(Business)\
            .join(Business.holder)\
            .where(Business.active)\
            .where(Business.id == id)\
            .options(joinedload(Business.holder))
        return session.scalars(stmt).first()
    
    @staticmethod
    def login(session:Session, login:Login):
        stmt = select(Business).join(Business.holder).where(Business.email == login.email).where(Business.password == login.password).options(joinedload(Business.holder))
        return session.scalars(stmt).first()
    
    @staticmethod
    def create(session:Session, business:BusinessCreate):
        business_dict = business.model_dump()
        for key, value in business_dict.copy().items():
            if value == None:
                del business_dict[key]
        stmt = insert(Business).values(**business_dict).returning(Business)
        with session.execute(stmt) as result:
            session.commit()
            return result.scalar_one()
        
    @staticmethod
    def update(session:Session, business:BusinessUpdate):
        business_dict = business.model_dump()
        for key, value in business_dict.copy().items():
            if value == None:
                del business_dict[key]
        stmt = update(Business).where(Business.active).where(Business.id == business.id).values(**business_dict).returning(Business)
        with session.execute(stmt) as result:
            session.commit()
            return result.scalar_one()
    
    @staticmethod
    def delete(session:Session, id: int):
        stmt = update(Business).where(Business.active).where(Business.id == id).values(active = False).returning(Business)
        with session.execute(stmt) as result:
            session.commit()
            return result.scalar_one()