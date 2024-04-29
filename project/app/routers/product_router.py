from fastapi import Depends, APIRouter, HTTPException, Path, Query
from typing import Annotated
from sqlmodel import Session
from ..database import get_db
from ..models import Product
from ..services.product_service import ProductService
from ..schemas.product_schema import ProductUpdate

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
    product:Product,
    db: Session = Depends(get_db),
    ):
    """Create: dada una información de body crea una entidad en base de datos.

    Args:
        product (Product): Objeto de sqlmodel tomado del body.
        db (Session, optional): Motor de base de datos. Defaults to Depends(get_db).

    Raises:
        HTTPException: Error de HTTP, da una respuesta con código.

    Returns:
        dict: Respuesta del servicio.
    """
    new_product = await ProductService.create(db, product)
    if not new_product:
        raise HTTPException(status_code = 500, detail = "Couldn't create product")
    return new_product

@router.put("/{id}")
async def update(
    id: Annotated[int, Path(title="ID of the product we want to update")],
    product:ProductUpdate,
    db: Session = Depends(get_db),
    ):
    """Update: Actualiza un registro según datos mutables y su id.

    Args:
        product (ProductUpdate): Objeto con los datos mutables.
        id (Annotated[int, Path, optional): Id de entidad. Defaults to "ID of the product we want to update")].
        db (Session, optional): Motor de base de datos. Defaults to Depends(get_db).

    Raises:
        HTTPException: Error de HTTP, da una respuesta con código.

    Returns:
        dict: Respuesta del servicio.
    """
    new_product = await ProductService.update(db, product, id)
    if not new_product:
        raise HTTPException(status_code = 500, detail = "Couldn't update product")
    return new_product

@router.delete("/{id}")
async def delete(
    id: Annotated[int, Path(title="ID of the product we want to deactivate")],
    db: Session = Depends(get_db),
    ):
    """Delete: Elimina un elemento según su id.

    Args:
        id (Annotated[int, Path, optional): Id de entidad. Defaults to "ID of the product we want to deactivate")].
        db (Session, optional): Motor de base de datos. Defaults to Depends(get_db).

    Raises:
        HTTPException: Error de HTTP, da una respuesta con código.

    Returns:
        dict: Respuesta del servicio.
    """
    new_product = await ProductService.delete(db, id)
    if not new_product:
        raise HTTPException(status_code = 500, detail = "Couldn't delete product")
    return new_product