from fastapi import Depends, APIRouter, HTTPException, Path, Query, status
from typing import Annotated
from sqlmodel import Session
from ..database import get_db
from ..models import Product
from ..services.product_service import ProductService
from ..schemas.product_schema import ProductUpdate
from ..helpers.security.security_helper import UserSecurityHelper
from ..models import User

# Aquí instancio el Router de producto para manejar sus respectivas peticiones.
router = APIRouter(prefix = "/product", tags = ['product'])

@router.get("/")
async def get_all(
    offset: Annotated[int, Query(title = "The page of product we want to get")] = 0,
    limit:  Annotated[int, Query(title = "The number of products we want to get per page")] = 10,
    db:Session = Depends(get_db),
    ):
    """Get all: Invoca al servicio para obtener todos los products.

    Args:
        offset (Annotated[int, Query, optional): Número de página. Defaults to "The page of product we want to get")]=0.
        limit (Annotated[int, Query, optional): Cantidad por página. Defaults to "The number of product we want to get per page")]=10.
        db (Session, optional): Motor de base de datos. Defaults to Depends(get_db).

    Returns:
        dict: Respuesta del servicio.
    """
    return await ProductService.get_all(db, offset, limit)

@router.get("/business/{id}")
async def get_by_business(
    id: Annotated[int, Path(title="ID of the product we want to find")],
    offset: Annotated[int, Query(title = "The page of product we want to get")] = 0,
    limit:  Annotated[int, Query(title = "The number of products we want to get per page")] = 10,
    db:Session = Depends(get_db),
    ):
    """Get by business: Invoca al servicio para obtener todos los products según un negocio.

    Args:
        id (Annotated[int, Path, optional): Id de negocio. Defaults to "ID of the product we want to find")].
        offset (Annotated[int, Query, optional): Número de página. Defaults to "The page of product we want to get")]=0.
        limit (Annotated[int, Query, optional): Cantidad por página. Defaults to "The number of product we want to get per page")]=10.
        db (Session, optional): Motor de base de datos. Defaults to Depends(get_db).

    Returns:
        dict: Respuesta del servicio.
    """
    return await ProductService.get_all(db, offset, limit, [
        Product.business_id == id 
    ])

@router.get("/{id}")
async def get_by_id(
    id: Annotated[int, Path(title="ID of the product we want to find")],
    db: Session = Depends(get_db),
    ):
    """Get by id: Dado un id, regresa su producto correspondiente 

    Args:
        id (Annotated[int, Path, optional): Id de entidad. Defaults to "ID of the product we want to find")].
        db (Session, optional): Motor de base de datos. Defaults to Depends(get_db).

    Raises:
        HTTPException: Error de HTTP, da una respuesta con código.

    Returns:
        dict: Respuesta del servicio.
    """
    product = await ProductService.get_by_id(db, id)
    if not product:
        raise HTTPException(status_code = 404, detail = "Product not found")
    return product

@router.post("/", status_code = 201)
async def create(
    current_user: Annotated[User, Depends(UserSecurityHelper.get_current)],
    product:Product,
    db: Session = Depends(get_db),
    ):
    """Create: dada una información de body crea una entidad en base de datos.

    Args:
        current_user (Annotated[User, Depends(UserSecurityHelper.get_current)): Usuario autenticado.
        product (Product): Objeto de sqlmodel tomado del body.
        db (Session, optional): Motor de base de datos. Defaults to Depends(get_db).

    Raises:
        HTTPException: Error de HTTP, da una respuesta con código.

    Returns:
        dict: Respuesta del servicio.
    """
    isAllowed = current_user.is_associated_with_business(product.business_id)
    if not isAllowed:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN , detail = "No tienes permiso para esta acción")
    new_product = await ProductService.create(db, product)
    if not new_product:
        raise HTTPException(status_code = 500, detail = "No se pudo crear producto")
    return new_product

@router.put("/{id}")
async def update(
    current_user: Annotated[User, Depends(UserSecurityHelper.get_current)],
    id: Annotated[int, Path(title="ID of the product we want to update")],
    product:ProductUpdate,
    db: Session = Depends(get_db),
    ):
    """Update: Actualiza un registro según datos mutables y su id.

    Args:
        current_user (Annotated[User, Depends(UserSecurityHelper.get_current)): Usuario autenticado.
        product (ProductUpdate): Objeto con los datos mutables.
        id (Annotated[int, Path, optional): Id de entidad. Defaults to "ID of the product we want to update")].
        db (Session, optional): Motor de base de datos. Defaults to Depends(get_db).

    Raises:
        HTTPException: Error de HTTP, da una respuesta con código.

    Returns:
        dict: Respuesta del servicio.
    """
    old_prod = await ProductService.get_by_id(db, id)
    isAllowed = current_user.is_associated_with_business(old_prod.business_id)
    if not isAllowed:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN , detail = "No tienes permiso para esta acción")
    new_product = await ProductService.update(db, product, id)
    if not new_product:
        raise HTTPException(status_code = 500, detail = "Couldn't update product")
    return new_product

@router.delete("/{id}")
async def delete(
    current_user: Annotated[User, Depends(UserSecurityHelper.get_current)],
    id: Annotated[int, Path(title="ID of the product we want to deactivate")],
    db: Session = Depends(get_db),
    ):
    """Delete: Elimina un elemento según su id.

    Args:
        current_user (Annotated[User, Depends(UserSecurityHelper.get_current)): Usuario autenticado.
        id (Annotated[int, Path, optional): Id de entidad. Defaults to "ID of the product we want to deactivate")].
        db (Session, optional): Motor de base de datos. Defaults to Depends(get_db).

    Raises:
        HTTPException: Error de HTTP, da una respuesta con código.

    Returns:
        dict: Respuesta del servicio.
    """
    old_prod = await ProductService.get_by_id(db, id)
    isAllowed = current_user.is_associated_with_business(old_prod.business_id)
    if not isAllowed:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN , detail = "No tienes permiso para esta acción")
    new_product = await ProductService.delete(db, id)
    if not new_product:
        raise HTTPException(status_code = 500, detail = "Couldn't delete product")
    return new_product