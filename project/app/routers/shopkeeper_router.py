from fastapi import Depends, APIRouter, HTTPException, Path, Query
from typing import Annotated
from sqlmodel import Session
from ..database import get_db
from ..models import Shopkeeper
from ..services.shopkeeper_service import ShopkeeperService
from ..schemas.shopkeeper_schema import ShopkeeperUpdate

# Aquí instancio el Router de tendero para manejar sus respectivas peticiones.
router = APIRouter(prefix = "/shopkeeper", tags = ['shopkeeper'])

@router.get("/")
async def get_all(
    offset: Annotated[int, Query(title = "The page of shopkeepers we want to get")] = 0,
    limit:  Annotated[int, Query(title = "The number of shopkeepers we want to get per page")] = 10,
    db:Session = Depends(get_db),
    ):
    """Get all: Invoca al servicio para obtener todos los shopkeepers.

    Args:
        offset (Annotated[int, Query, optional): Número de página. Defaults to "The page of shopkeeper we want to get")]=0.
        limit (Annotated[int, Query, optional): Cantidad por página. Defaults to "The number of shopkeeper we want to get per page")]=10.
        db (Session, optional): Motor de base de datos. Defaults to Depends(get_db).

    Returns:
        dict: Respuesta del servicio.
    """
    return await ShopkeeperService.get_all(db, offset, limit)

@router.get("/{id}")
async def get_by_id(
    id: Annotated[int, Path(title="ID of the shopkeeper we want to find")],
    db: Session = Depends(get_db),
    ):
    """Get by id: Dado un id, regresa su shopkeeper correspondiente 

    Args:
        id (Annotated[int, Path, optional): Id de entidad. Defaults to "ID of the shopkeeper we want to find")].
        db (Session, optional): Motor de base de datos. Defaults to Depends(get_db).

    Raises:
        HTTPException: Error de HTTP, da una respuesta con código.

    Returns:
        dict: Respuesta del servicio.
    """
    shopkeeper = await ShopkeeperService.get_by_id(db, id)
    if not shopkeeper:
        raise HTTPException(status_code = 404, detail = "shopkeeper not found")
    return shopkeeper

@router.post("/", status_code = 201)
async def create(
    shopkeeper:Shopkeeper,
    db: Session = Depends(get_db),
    ):
    """Create: dada una información de body crea una entidad en base de datos.

    Args:
        shopkeeper (Shopkeeper): Objeto de sqlmodel tomado del body.
        db (Session, optional): Motor de base de datos. Defaults to Depends(get_db).

    Raises:
        HTTPException: Error de HTTP, da una respuesta con código.

    Returns:
        dict: Respuesta del servicio.
    """
    new_shopkeeper = await ShopkeeperService.create(db, shopkeeper)
    if not new_shopkeeper:
        raise HTTPException(status_code = 500, detail = "couldn't create shopkeeper")
    return new_shopkeeper

@router.put("/{id}")
async def update(
    id: Annotated[int, Path(title="ID of the shopkeeper we want to update")],
    shopkeeper:ShopkeeperUpdate,
    db: Session = Depends(get_db),
    ):
    """Update: Actualiza un registro según datos mutables y su id.

    Args:
        shopkeeper (ShopkeeperUpdate): Objeto con los datos mutables.
        id (Annotated[int, Path, optional): Id de entidad. Defaults to "ID of the shopkeeper we want to update")].
        db (Session, optional): Motor de base de datos. Defaults to Depends(get_db).

    Raises:
        HTTPException: Error de HTTP, da una respuesta con código.

    Returns:
        dict: Respuesta del servicio.
    """
    new_shopkeeper = await ShopkeeperService.update(db, shopkeeper, id)
    if not new_shopkeeper:
        raise HTTPException(status_code = 500, detail = "couldn't update shopkeeper")
    return new_shopkeeper

@router.delete("/{id}")
async def delete(
    id: Annotated[int, Path(title="ID of the shopkeeper we want to deactivate")],
    db: Session = Depends(get_db),
    ):
    """Delete: Elimina un elemento según su id.

    Args:
        id (Annotated[int, Path, optional): Id de entidad. Defaults to "ID of the shopkeeper we want to deactivate")].
        db (Session, optional): Motor de base de datos. Defaults to Depends(get_db).

    Raises:
        HTTPException: Error de HTTP, da una respuesta con código.

    Returns:
        dict: Respuesta del servicio.
    """
    new_shopkeeper = await ShopkeeperService.delete(db, id)
    if not new_shopkeeper:
        raise HTTPException(status_code = 500, detail = "couldn't delete shopkeeper")
    return new_shopkeeper