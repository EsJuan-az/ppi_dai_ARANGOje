from ..models import Shopkeeper
from ..schemas import ShopkeeperCreate, ShopkeeperUpdate
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, update

class ShopkeeperService:
    @staticmethod
    def get_all(session:Session, offset:int, limit:int):
        stmt = select(Shopkeeper)\
            .join(Shopkeeper.business)\
            .where(Shopkeeper.active)\
            .offset(offset)\
            .limit(limit)
        return session.scalars(stmt).all()
    
    @staticmethod
    def get_by_id(session:Session, id:int):
        stmt = select(Shopkeeper)\
            .join(Shopkeeper.business)\
            .where(Shopkeeper.active)\
            .where(Shopkeeper.id == id)
        return session.scalars(stmt).first()
    
    @staticmethod
    def create(session:Session, shopkeeper:ShopkeeperCreate):
        shopkeeper_dict = shopkeeper.model_dump()
        for key, value in shopkeeper_dict.copy().items():
            if value == None:
                del shopkeeper_dict[key]
        stmt = insert(Shopkeeper).values(**shopkeeper_dict).returning(Shopkeeper)
        with session.execute(stmt) as result:
            session.commit()
            return result.scalar_one()
        
    @staticmethod
    def update(session:Session, shopkeeper:ShopkeeperUpdate):
        shopkeeper_dict = shopkeeper.model_dump()
        for key, value in shopkeeper_dict.copy().items():
            if value == None:
                del shopkeeper_dict[key]
        stmt = update(Shopkeeper).where(Shopkeeper.active).where(Shopkeeper.id == shopkeeper.id).values(**shopkeeper_dict).returning(Shopkeeper)
        with session.execute(stmt) as result:
            session.commit()
            return result.scalar_one()
    
    @staticmethod
    def delete(session:Session, id: int):
        stmt = update(Shopkeeper).where(Shopkeeper.active).where(Shopkeeper.id == id).values(active = False).returning(Shopkeeper)
        with session.execute(stmt) as result:
            session.commit()
            return result.scalar_one()