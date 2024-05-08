from ..models import Base
from pydantic import BaseModel
from sqlmodel import select, Session, exists
from sqlalchemy.orm import joinedload



class BaseService:
    """Servicio base para el CRUD de entidades en base de datos.
    Args:
        model (Base): Modelo de base de datos a consular.
        update_model (Pydantic.BaseModel): Modelo de actualización de pydantic.
        get_all_join_attrs (list[str]): Lista de relaciones a traer en cada get_all.
        get_one_join_attrs (list[str]): Lista de relaciones a traer en cada get_one.
    """
    def __init__(self, model=Base, update_model=BaseModel, get_all_join_attrs=[], get_one_join_attrs=[]):
        self.model = model
        self.update_model = update_model
        self.get_all_join_attrs = get_all_join_attrs
        self.get_one_join_attrs = get_one_join_attrs
    
    @staticmethod
    async def exist(session:Session, query:list = []):
        """Exist: Confirma si existe una entidad con una condición.

        Args:
            session (Session): Sesión de base de datos.
            offset (int): Página.
            limit (int): Entidades por página.

        Returns:
           list[dict]: Arreglo con todas las entidades.
        """
        stmt = exists()
        for condition in query:
            stmt = stmt.where(condition)
        stmt = select(stmt)
        result = await session.exec(stmt)
        return result.scalar() 
    
    
    async def get_all(self, session:Session, offset:int, limit:int, query:list = []):
        """Get all: obtiene todas las entidades

        Args:
            session (Session): Sesión de base de datos.
            offset (int): Página.
            limit (int): Entidades por página.
            query (list): Lista de condiciones a aplicar.

        Returns:
           list[dict]: Arreglo con todas las entidades.
        """
        join_attrs = [getattr(self.model, attr) for attr in self.get_all_join_attrs] 
        stmt = select(self.model)
        if len(join_attrs) > 0:
            stmt = stmt.options(*[joinedload(attr) for attr in join_attrs])
        for attr in join_attrs:
            stmt = stmt.join(attr)
        for condition in query:
            stmt = stmt.where(condition)
        stmt = stmt.offset(offset)\
            .limit(limit)
        result = await session.exec(stmt)
        return result.all()
    
    async def get_by_pk(self, session:Session, query:list = []):
        """Get all: obtiene todas las entidades

        Args:
            session (Session): Sesión de base de datos.
            offset (int): Página.
            limit (int): Entidades por página.
            query (list): Lista de condiciones a aplicar.

        Returns:
           list[dict]: Arreglo con todas las entidades.
        """
        join_attrs = [getattr(self.model, attr) for attr in self.get_all_join_attrs] 
        stmt = select(self.model)
        if len(join_attrs) > 0:
            stmt = stmt.options(*[joinedload(attr) for attr in join_attrs])
        for attr in join_attrs:
            stmt = stmt.join(attr)
        for condition in query:
            stmt = stmt.where(condition)
        result = await session.exec(stmt)
        return result.one()
    
    async def get_by_id(self, session:Session, id:int):
        """Get by id: dado un id retorna la entidad correspondiente.

        Args:
            session (Session): Sesión de base.
            id (int): Id de entidad

        Returns:
            model: Objeto que cumpla la condición.
        """
        join_attrs = [getattr(self.model, attr) for attr in self.get_one_join_attrs] 
        stmt = select(self.model)
        for attr in join_attrs:
            stmt = stmt.options(joinedload(attr))
        for attr in join_attrs:
            stmt = stmt.join(attr)
        stmt = stmt.where(self.model.id == id)
        result = await session.exec(stmt)
        return result.one()    
    
    async def create(self, session:Session, entity):
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
        
    async def update(self, session:Session, entity, id: int):
        """Update: dado una id y un objeto de datos, actualiza la entidad.

        Args:
            session (Session): Sesión de base.
            entity (update_model): Objeto de datos.
            id (int): Id de entidad.

        Returns:
            model: Entidad actualizada.
        """
        entity_dict = entity.model_dump()
        new_entity = await self.get_by_id(session, id)
        for key, val in entity_dict.items():
            if val is None:
                continue
            new_entity.__setattr__(key, val)
        session.add(new_entity);
        await session.commit()
        await session.refresh(new_entity)
        return new_entity
        
    
    async def delete(self, session:Session, id: int):
        """Delete: dado una id desactiva la entidad.

        Args:
            session (Session): Sesión de base de datos.
            id (int): Id de entidad.

        Returns:
            model: Regresa el objeto eliminado.
        """
        entity = await self.get_by_id(session, id)
        session.delete(new_entity);
        await session.commit()
        return True