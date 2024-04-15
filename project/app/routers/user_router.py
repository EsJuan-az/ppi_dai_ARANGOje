from fastapi import Depends, APIRouter, HTTPException, Path, Query
from typing import Annotated
from sqlmodel import Session
from ..database import get_db

from ..services.user_service import UserService

from ..models import User
from ..schemas.user_schema import UserUpdate
from ..schemas.login_schema import Login

router = APIRouter(prefix = "/user", tags = ['user'])

@router.get("/")
async def get_all(
    offset: Annotated[int, Query(title = "the page of user we want to get")] = 0,
    limit:  Annotated[int, Query(title = "the number of users we want to get per page")] = 10,
    db:Session = Depends(get_db),
    ):
    """Get all: Invoca al servicio para obtener todos los user.

    Args:
        offset (Annotated[int, Query, optional): Número de página. Defaults to "The page of users we want to get")]=0.
        limit (Annotated[int, Query, optional): Cantidad por página. Defaults to "The number of users we want to get per page")]=10.
        db (Session, optional): Motor de base de datos. Defaults to Depends(get_db).

    Returns:
        dict: Respuesta del servicio.
    """
    return await UserService.get_all(db, offset, limit)

@router.get("/{id}")
async def get_by_id(
    id: Annotated[int, Path(title="ID of the user we want to find")],
    db: Session = Depends(get_db),
    ):
    """Get by id: Dado un id, regresa su user correspondiente 

    Args:
        id (Annotated[int, Path, optional): Id de entidad. Defaults to "ID of the user we want to find")].
        db (Session, optional): Motor de base de datos. Defaults to Depends(get_db).

    Raises:
        HTTPException: Error de HTTP, da una respuesta con código.

    Returns:
        dict: Respuesta del servicio.
    """
    user = await UserService.get_by_id(db, id)
    if not user:
        raise HTTPException(status_code = 404, detail = "user not found")
    return user

@router.post("/", status_code = 201)
async def create(
    user:User,
    db: Session = Depends(get_db),
    ):
    """Create: dada una información de body crea una entidad en base de datos.

    Args:
        user (UserUpdate): Objeto de sqlmodel tomado del body.
        db (Session, optional): Motor de base de datos. Defaults to Depends(get_db).

    Raises:
        HTTPException: Error de HTTP, da una respuesta con código.

    Returns:
        dict: Respuesta del servicio.
    """
    new_user = await UserService.create(db, user)
    if not new_user:
        raise HTTPException(status_code = 500, detail = "couldn't create User")
    return new_user

@router.post('/auth')
async def login(
    login: Login,
    db: Session = Depends(get_db),
    ):
    """Login: dado un email y su contraseña, autentifica y regresa una empresa.

    Args:
        login (Login): Objeto con email y contraseña.
        db (Session, optional): Motor de base de datos. Defaults to Depends(get_db).

    Raises:
        HTTPException: Error de HTTP, da una respuesta con código.

    Returns:
        dict: Respuesta del servicio.
    """
    user = await UserService.login(db, login)
    if not user:
        raise HTTPException(status_code = 403, detail = "invalid credentials")
    return user

@router.put("/{id}")
async def update(
    id: Annotated[int, Path(title="ID of the user we want to update")],
    user:UserUpdate,
    db: Session = Depends(get_db),
    ):
    """Update: Actualiza un registro según datos mutables y su id.

    Args:
        user (UserUpdate): Objeto con los datos mutables.
        id (Annotated[int, Path, optional): Id de entidad. Defaults to "ID of the user we want to update")].
        db (Session, optional): Motor de base de datos. Defaults to Depends(get_db).

    Raises:
        HTTPException: Error de HTTP, da una respuesta con código.

    Returns:
        dict: Respuesta del servicio.
    """
    new_user = await UserService.update(db, user, id)
    if not new_user:
        raise HTTPException(status_code = 500, detail = "couldn't update User")
    return new_user

@router.delete("/{id}")
async def delete(
    id: Annotated[int, Path(title="ID of the user we want to deactivate")],
    db: Session = Depends(get_db),
    ):
    """Delete: Elimina un elemento según su id.

    Args:
        id (Annotated[int, Path, optional): Id de entidad. Defaults to "ID of the user we want to deactivate")].
        db (Session, optional): Motor de base de datos. Defaults to Depends(get_db).

    Raises:
        HTTPException: Error de HTTP, da una respuesta con código.

    Returns:
        dict: Respuesta del servicio.
    """
    new_user = await UserService.delete(db, id)
    if not new_user:
        raise HTTPException(status_code = 500, detail = "couldn't delete User")
    return new_user
