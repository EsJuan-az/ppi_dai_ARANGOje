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
        """Get all: obtiene todas las entidades

        Args:
            session (Session): Sesión de base de datos.
            offset (int): Página.
            limit (int): Entidades por página.

        Returns:
           list[dict]: Arreglo con todas las entidades.
        """
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
        """Get by id: dado un id retorna la entidad correspondiente.

        Args:
            session (Session): Sesión de base.
            id (int): Id de entidad

        Returns:
            model: Objeto que cumpla la condición.
        """
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
        """Create: dado un objeto de body, crea una entidad en base y la guarda.

        Args:
            session (Session): Sesión de base de datos.
            entity (model): Datos del body para generar la base.

        Returns:
            model: Objeto creado.
        """
        session.add(entity)
        await session.commit()
        await session.refresh(entity)
        return entity
        
    @classmethod
    async def update(cls, session:Session, entity:update_model, id: int) -> model:
        """Update: dado una id y un objeto de datos, actualiza la entidad.

        Args:
            session (Session): Sesión de base.
            entity (update_model): Objeto de datos.
            id (int): Id de entidad.

        Returns:
            model: Entidad actualizada.
        """
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
        """Delete: dado una id desactiva la entidad.

        Args:
            session (Session): Sesión de base de datos.
            id (int): Id de entidad.

        Returns:
            model: Regresa el objeto eliminado.
        """
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