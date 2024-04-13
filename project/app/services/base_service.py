from ..models import Base
from pydantic import BaseModel
from sqlmodel import select, Session



class BaseService:
    model = Base
    update_model = BaseModel
    get_all_join_attrs = []
    get_one_join_attrs = []
    
    @classmethod
    async def get_all(cls, session:Session, offset:int, limit:int):
        stmt = select(cls.model)
        for joinAttr in cls.get_all_join_attrs:
            attr = getattr(cls.model, joinAttr)
            stmt = stmt.join(attr)
        stmt = stmt.where(cls.model.active)
        stmt = stmt.offset(offset)\
            .limit(limit)
        result = await session.exec(stmt)
        return result.all()
    
    @classmethod
    async def get_by_id(cls, session:Session, id:int) -> model:
        stmt = select(cls.model)
        for joinAttr in cls.get_one_join_attrs:
            attr = getattr(cls.model, joinAttr)
            stmt = stmt.join(attr)
        stmt = stmt.where(cls.model.active)\
            .where(cls.model.id == id)
        result = await session.exec(stmt)
        return result.one()    
    
    @classmethod
    async def create(cls, session:Session, entity:model) -> model:
        session.add(entity)
        await session.commit()
        await session.refresh(entity)
        return entity
        
    @classmethod
    async def update(cls, session:Session, entity:update_model, id: int) -> model:
        entity_dict = entity.model_dump()
        print(entity_dict)
        stmt = select(cls.model)\
            .where(cls.model.active)\
            .where(cls.model.id == id)
        new_entity = await session.exec(stmt)
        new_entity = new_entity.one()
        for key, val in entity_dict.items():
            if val is None:
                continue
            new_entity.__setattr__(key, val)
        session.add(new_entity);
        await session.commit()
        await session.refresh(new_entity)
        return new_entity
        
    
    @classmethod
    async def delete(cls, session:Session, id: int) -> model:
        stmt = select(cls.model)\
            .where(cls.model.active)\
            .where(cls.model.id == id)
        new_entity = await session.exec(stmt)
        new_entity = new_entity.one()
        new_entity.active = False
        session.add(new_entity);
        await session.commit()
        await session.refresh(new_entity)
        return new_entity