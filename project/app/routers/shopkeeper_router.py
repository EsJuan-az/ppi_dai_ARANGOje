from fastapi import Depends, APIRouter, HTTPException, Path, Query, status
from typing import Annotated
from sqlmodel import Session
from ..database import get_db
from ..models import Shopkeeper
from ..services.shopkeeper_service import ShopkeeperService
from ..schemas.shopkeeper_schema import ShopkeeperUpdate
from ..helpers.security.security_helper import UserSecurityHelper
from ..models import User
# Aquí instancio el Router de tendero para manejar sus respectivas peticiones.
router = APIRouter(prefix = "/shopkeeper", tags = ['shopkeeper'])

@router.get("/{id}")
async def get_by_id(
    id: Annotated[int, Path(title="ID of the shopkeeper we want to find")],
    offset: Annotated[int, Query(title = "The page of product we want to get")] = 0,
    limit:  Annotated[int, Query(title = "The number of products we want to get per page")] = 30,
    db: Session = Depends(get_db),
    ):
    """Get by id: Dado un id, regresa los shopkeepers de este negocio. 

    Args:
        id (Annotated[int, Path, optional): Id de negocio. Defaults to "ID of the shopkeeper we want to find")].
        offset (Annotated[int, Query, optional): Número de página. Defaults to "The page of product we want to get")]=0.
        limit (Annotated[int, Query, optional): Cantidad por página. Defaults to "The number of product we want to get per page")]=10.
        db (Session, optional): Motor de base de datos. Defaults to Depends(get_db).

    Raises:
        HTTPException: Error de HTTP, da una respuesta con código.

    Returns:
        dict: Respuesta del servicio.
    """
    return await ShopkeeperService.get_all(db, offset, limit, [
        Shopkeeper.business_id == id,
    ])

@router.post("/", status_code = 201)
async def create(
    current_user: Annotated[User, Depends(UserSecurityHelper.get_current)],
    shopkeeper:Shopkeeper,
    db: Session = Depends(get_db),
    ):
    """Create: dada una información de body crea una entidad en base de datos.

    Args:
        current_user (Annotated[User, Depends(UserSecurityHelper.get_current)): Usuario autenticado.
        shopkeeper (Shopkeeper): Objeto de sqlmodel tomado del body.
        db (Session, optional): Motor de base de datos. Defaults to Depends(get_db).

    Raises:
        HTTPException: Error de HTTP, da una respuesta con código.

    Returns:
        dict: Respuesta del servicio.
    """
    isAllowed = current_user.is_associated_with_business(shopkeeper.business_id)
    if not isAllowed:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN , detail = "No tienes permiso para esta acción")
    new_shopkeeper = await ShopkeeperService.create(db, shopkeeper)
    if not new_shopkeeper:
        raise HTTPException(status_code = 500, detail = "No se pudo añadir Tendero")
    return new_shopkeeper

@router.delete("/{id}")
async def delete(
    current_user: Annotated[User, Depends(UserSecurityHelper.get_current)],
    id: Annotated[int, Path(title="ID of the shopkeeper we want to deactivate")],
    db: Session = Depends(get_db),
    ):
    """Delete: Elimina un elemento según su id.

    Args:
        current_user (Annotated[User, Depends(UserSecurityHelper.get_current)): Usuario autenticado.
        id (Annotated[int, Path, optional): Id de entidad. Defaults to "ID of the shopkeeper we want to deactivate")].
        db (Session, optional): Motor de base de datos. Defaults to Depends(get_db).

    Raises:
        HTTPException: Error de HTTP, da una respuesta con código.

    Returns:
        dict: Respuesta del servicio.
    """
    shopkeeper = await ShopkeeperService.get_by_id(db, id)
    isAllowed = current_user.is_associated_with_business(shopkeeper.business_id)
    if not isAllowed:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN , detail = "No tienes permiso para esta acción")
    new_shopkeeper = await ShopkeeperService.delete(db, id)
    if not new_shopkeeper:
        raise HTTPException(status_code = 500, detail = "couldn't delete shopkeeper")
    return new_shopkeeper