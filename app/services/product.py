from ..models import Product
from ..schemas import ProductCreate, ProductUpdate
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, update

class ProductService:
    @staticmethod
    def get_all(session:Session, offset:int, limit:int):
        stmt = select(Product)\
            .join(Product.business)\
            .where(Product.active)\
            .offset(offset)\
            .limit(limit)
        return session.scalars(stmt).all()
    
    @staticmethod
    def get_by_id(session:Session, id:int):
        stmt = select(Product)\
            .join(Product.business)\
            .where(Product.active)\
            .where(Product.id == id)
        return session.scalars(stmt).first()
    
    @staticmethod
    def create(session:Session, product:ProductCreate):
        product_dict = product.model_dump()
        for key, value in product_dict.copy().items():
            if value == None:
                del product_dict[key]
        stmt = insert(Product).values(**product_dict).returning(Product)
        with session.execute(stmt) as result:
            session.commit()
            return result.scalar_one()
        
    @staticmethod
    def update(session:Session, product:ProductUpdate):
        product_dict = product.model_dump()
        for key, value in product_dict.copy().items():
            if value == None:
                del product_dict[key]
        stmt = update(Product).where(Product.active).where(Product.id == product.id).values(**product_dict).returning(Product)
        with session.execute(stmt) as result:
            session.commit()
            return result.scalar_one()
    
    @staticmethod
    def delete(session:Session, id: int):
        stmt = update(Product).where(Product.active).where(Product.id == id).values(active = False).returning(Product)
        with session.execute(stmt) as result:
            session.commit()
            return result.scalar_one()