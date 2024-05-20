from fastapi import Depends, APIRouter, HTTPException, Path, Query, status
from typing import Annotated
from sqlmodel import Session
from ..database import get_db
# Servicios a consumir
from ..services.order_service import OrderService
from ..services.order_product_service import OrderProductService
from ..services.product_service import ProductService

# Helpers y tipos de datos.
from ..schemas.order_schema import OrderUpdate, RemoveProduct
from ..schemas.base_schema import Position

from ..helpers.security.security_helper import UserSecurityHelper
from ..helpers.data_helper import DataHelper
from ..models import User, Order, OrderProduct
import osmnx as ox
import networkx as nx
import io
from PIL import Image
import base64
from shapely.geometry import Point
from ..models import Record
from ..services.record_service import RecordService


# Aquí instancio el Router de negocio para manejar sus respectivas peticiones.
router = APIRouter(prefix = "/order", tags = ['order'])

    
@router.get("/")
async def get_all(
    current_user: Annotated[User, Depends(UserSecurityHelper.get_current)],
    offset: Annotated[int, Query(title = "The page of order we want to get")] = 0,
    limit:  Annotated[int, Query(title = "The number of orders we want to get per page")] = 30,
    db:Session = Depends(get_db),
    ):
    """Get all: Invoca al servicio para obtener todos las ordenes propias.

    Args:
        current_user (Annotated[User, Depends(UserSecurityHelper.get_current)): Usuario autenticado.
        offset (Annotated[int, Query, optional): Número de página. Defaults to "The page of order we want to get")]=0.
        limit (Annotated[int, Query, optional): Cantidad por página. Defaults to "The number of orders we want to get per page")]=10.
        db (Session, optional): Motor de base de datos. Defaults to Depends(get_db).

    Returns:
        dict: Respuesta del servicio.
    """
    
    orders = await OrderService.get_all(db, offset, limit, [
        Order.customer_id == current_user.id,
        ])
    
    return [
        {
            "updated_at": order.updated_at,
            "customer_id": order.customer_id,
            "business_id": order.business_id,
            "lon": order.lon,
            "status": order.status,
            "created_at": order.created_at,
            "id": order.id,
            "lat": order.lat,
            "customer": order.customer,
            "business": order.business,
            "products": order.products
        } for order in orders]

@router.post("/map")
async def get_all_map(
    current_user: Annotated[User, Depends(UserSecurityHelper.get_current)],
    position: Position,
    offset: Annotated[int, Query(title = "The page of order we want to get")] = 0,
    limit:  Annotated[int, Query(title = "The number of orders we want to get per page")] = 30,
    db:Session = Depends(get_db),
    ):
    """Get all map: Invoca al servicio para obtener un mapa con todos los puntos.

    Args:
        current_user (Annotated[User, Depends(UserSecurityHelper.get_current)): Usuario autenticado.
        offset (Annotated[int, Query, optional): Número de página. Defaults to "The page of order we want to get")]=0.
        limit (Annotated[int, Query, optional): Cantidad por página. Defaults to "The number of orders we want to get per page")]=10.
        db (Session, optional): Motor de base de datos. Defaults to Depends(get_db).

    Returns:
        dict: Respuesta del servicio.
    """
    
    orders = await OrderService.get_all(db, offset, limit, [
        Order.business_id.in_(current_user.associated_business_ids),
        ])
    start_point = Point(position.lon, position.lat)
    other_points = [Point(o.lon, o.lat) for o in orders]
    
    dictorder = {}
    route = DataHelper.tsp(start_point, other_points)
    fig, ax = DataHelper.plot_route(route)

    # Añadir un mapa de fondo usando contextily
    # ctx.add_basemap(ax, source=ctx.providers.Stamen.TonerLite, zoom=12, crs=G.graph['crs'])

    # Convertir el gráfico a Data URL
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    image = Image.open(buf)
    data = io.BytesIO()
    image.save(data, "PNG")
    dictorder['map'] = "data:image/png;base64," + base64.b64encode(data.getvalue()).decode()

    # Cerrar el buffer
    buf.close()

    return dictorder

@router.get("/business")
async def get_bsns(
    current_user: Annotated[User, Depends(UserSecurityHelper.get_current)],
    offset: Annotated[int, Query(title = "The page of order we want to get")] = 0,
    limit:  Annotated[int, Query(title = "The number of orders we want to get per page")] = 30,
    db:Session = Depends(get_db),
    ):
    """Get by business: Invoca al servicio para obtener todos las ordenes de un negocio en particular.

    Args:
        current_user (Annotated[User, Depends(UserSecurityHelper.get_current)): Usuario autenticado.
        offset (Annotated[int, Query, optional): Número de página. Defaults to "The page of order we want to get")]=0.
        limit (Annotated[int, Query, optional): Cantidad por página. Defaults to "The number of orders we want to get per page")]=10.
        db (Session, optional): Motor de base de datos. Defaults to Depends(get_db).

    Returns:
        dict: Respuesta del servicio.
    """
    orders = await OrderService.get_all(db, offset, limit, [
        Order.business_id.in_(current_user.associated_business_ids),
        ])
    return [
        {
            "updated_at": order.updated_at,
            "customer_id": order.customer_id,
            "business_id": order.business_id,
            "lon": order.lon,
            "status": order.status,
            "created_at": order.created_at,
            "id": order.id,
            "lat": order.lat,
            "customer": order.customer,
            "business": order.business,
            "total_price": order.total_price,
            "products": order.products
        } for order in orders]



@router.get("/{id}")
async def get_by_id(
    current_user: Annotated[User, Depends(UserSecurityHelper.get_current)],
    id: Annotated[int, Path(title="ID of the order we want to find")],
    db: Session = Depends(get_db),
    ):
    """Get by id: Dado un id, regresa su orden correspondiente 

    Args:
        current_user (Annotated[User, Depends(UserSecurityHelper.get_current)): Usuario autenticado.
        id (Annotated[int, Path, optional): Id de entidad. Defaults to "ID of the business we want to find")].
        db (Session, optional): Motor de base de datos. Defaults to Depends(get_db).

    Raises:
        HTTPException: Error de HTTP, da una respuesta con código.

    Returns:
        dict: Respuesta del servicio.
    """
    order = await OrderService.get_by_id(db, id)
    isAllowed = current_user.is_associated_with_business(order.business_id)
    if not isAllowed:
        raise HTTPException(status_code = 404, detail = "Orden no encontrada")
    
    dictorder = order.__dict__
    # Obtenemos productos y precio total.
    dictorder['products'] = order.products
    dictorder['total_price'] = order.total_price
    return dictorder
    
@router.post('/map/{id}')
async def get_map(
    current_user: Annotated[User, Depends(UserSecurityHelper.get_current)],
    position: Position,
    id: Annotated[int, Path(title="ID of the order we want to find")],
    db: Session = Depends(get_db),
    ):
    """Get by id: Dado un id, regresa su orden correspondiente 

    Args:
        current_user (Annotated[User, Depends(UserSecurityHelper.get_current)): Usuario autenticado.
        id (Annotated[int, Path, optional): Id de entidad. Defaults to "ID of the business we want to find")].
        db (Session, optional): Motor de base de datos. Defaults to Depends(get_db).

    Raises:
        HTTPException: Error de HTTP, da una respuesta con código.

    Returns:
        dict: Respuesta del servicio.
    """
    order = await OrderService.get_by_id(db, id)
    isAllowed = current_user.is_associated_with_business(order.business_id)
    if not isAllowed:
        raise HTTPException(status_code = 404, detail = "Orden no encontrada")
    
    dictorder = order.__dict__
    # Coordenadas
    start = Point(order.lon, order.lat)  # Punto de inicio (orden)
    end = Point(position.lon, position.lat)  # Punto final (posición actual)
    
    dictorder = {}
    route = DataHelper.tsp(start, [end])
    fig, ax = DataHelper.plot_route(route)

    # Añadir un mapa de fondo usando contextily
    # ctx.add_basemap(ax, source=ctx.providers.Stamen.TonerLite, zoom=12, crs=G.graph['crs'])

    # Convertir el gráfico a Data URL
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    image = Image.open(buf)
    data = io.BytesIO()
    image.save(data, "PNG")
    dictorder['map'] = "data:image/png;base64," + base64.b64encode(data.getvalue()).decode()

    # Cerrar el buffer
    buf.close()

    return dictorder

@router.get("/business/{business_id}")
async def get_me(
    current_user: Annotated[User, Depends(UserSecurityHelper.get_current)],
    business_id: Annotated[int, Path(title="ID of the order we want to find")],
    offset: Annotated[int, Query(title = "The page of order we want to get")] = 0,
    limit:  Annotated[int, Query(title = "The number of orders we want to get per page")] = 30,
    db: Session = Depends(get_db),
    ):
    """Get by business: Dado un id de un negocio, regresa sus ordenes correspondientes. 

    Args:
        current_user (Annotated[User, Depends(UserSecurityHelper.get_current)): Usuario autenticado.
        business_id (Annotated[int, Path, optional): Id de entidad. Defaults to "ID of the order we want to find")].
        db (Session, optional): Motor de base de datos. Defaults to Depends(get_db).
        offset (Annotated[int, Query(title = "The page of order we want to get")]): Página.,
        limit  (Annotated[int, Query(title = "The number of orders we want to get per page")]): Cantidad por página,

    Raises:
        HTTPException: Error de HTTP, da una respuesta con código.

    Returns:
        dict: Respuesta del servicio.
    """
    isAllowed = current_user.is_associated_with_business(business_id)
    if not isAllowed:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN , detail = "No tienes permiso para esta acción")
    return await OrderService.get_all(db, offset, limit, [
        Order.business_id == business_id
    ])




@router.post("/", status_code = 201)
async def create(
    current_user: Annotated[User, Depends(UserSecurityHelper.get_current)],
    order:Order,
    db: Session = Depends(get_db),
    ):
    """Create: dada una información de body crea una entidad en base de datos.

    Args:
        current_user (Annotated[User, Depends(UserSecurityHelper.get_current)): Usuario autenticado.
        business (Business): Objeto de sqlmodel tomado del body.
        db (Session, optional): Motor de base de datos. Defaults to Depends(get_db).

    Raises:
        HTTPException: Error de HTTP, da una respuesta con código.

    Returns:
        dict: Respuesta del servicio.
    """
    order.customer_id = current_user.id
    new_order = await OrderService.create(db, order)
    if not new_order:
        raise HTTPException(status_code = 500, detail = "No se pudo crear esta orden")
    record = Record(
        business_id=new_order.business_id,
        user_id=current_user.id,
        raw_message='$uname$ hizo una orden a $bname$',
    )
    await RecordService.create(db, record)
    return new_order


@router.put("/{id}")
async def update(
    current_user: Annotated[User, Depends(UserSecurityHelper.get_current)],
    id: Annotated[int, Path(title="ID of the order we want to update")],
    orderUp:OrderUpdate,
    db: Session = Depends(get_db),
    ):
    """Update: Actualiza un registro según datos mutables y su id.

    Args:
        current_user (Annotated[User, Depends(UserSecurityHelper.get_current)): Usuario autenticado.
        order (OrderUpdate): Objeto con los datos mutables.
        id (Annotated[int, Path, optional): Id de entidad. Defaults to "ID of the order we want to update")].
        db (Session, optional): Motor de base de datos. Defaults to Depends(get_db).

    Raises:
        HTTPException: Error de HTTP, da una respuesta con código.

    Returns:
        dict: Respuesta del servicio.
    """
    order = await OrderService.get_by_id(db, id)
    isAllowed = current_user.is_associated_with_business(order.business_id)
    if not isAllowed:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN , detail = "No tienes permiso para esta acción")
    new_order = await OrderService.update(db, orderUp, id)
    if not new_order:
        raise HTTPException(status_code = 500, detail = "No se pudo actualizar la orden")
    return new_order

@router.delete("/{id}")
async def delete(
    current_user: Annotated[User, Depends(UserSecurityHelper.get_current)],
    id: Annotated[int, Path(title="ID of the order we want to deactivate")],
    db: Session = Depends(get_db),
    ):
    """Delete: Elimina un elemento según su id.

    Args:
        current_user (Annotated[User, Depends(UserSecurityHelper.get_current)): Usuario autenticado.
        id (Annotated[int, Path, optional): Id de entidad. Defaults to "ID of the order we want to deactivate")].
        db (Session, optional): Motor de base de datos. Defaults to Depends(get_db).

    Raises:
        HTTPException: Error de HTTP, da una respuesta con código.

    Returns:
        dict: Respuesta del servicio.
    """
    order = await OrderService.get_by_id(db, id)
    isAllowed = current_user.is_associated_with_business(order.business_id)
    if not isAllowed:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN , detail = "No tienes permiso para esta acción")
    new_order = await OrderService.delete(db, id)
    if not new_order:
        raise HTTPException(status_code = 500, detail = "No se pudo eliminar la orden")
    return new_order

@router.post("/product/")
async def add_product(
    current_user: Annotated[User, Depends(UserSecurityHelper.get_current)],
    upserts: OrderProduct,
    db: Session = Depends(get_db),
    ):
    """Add product by id: Dado un id, añade un producto a la orden.
    Args:
        current_user (Annotated[User, Depends(UserSecurityHelper.get_current)): Usuario autenticado.
        upserts (OrderProduct): Datos del producto y cantidad.,
        id (Annotated[int, Path, optional): Id de entidad. Defaults to "ID of the order we want to find")].
        db (Session, optional): Motor de base de datos. Defaults to Depends(get_db).

    Raises:
        HTTPException: Error de HTTP, da una respuesta con código.

    Returns:
        dict: Respuesta del servicio.
    """
    product = await ProductService.get_by_id(db, upserts.product_id)
    order = await OrderService.get_by_id(db, upserts.order_id)
    isAllowed = current_user.id == order.customer_id
    if not isAllowed or product.business_id != order.business_id:
        raise HTTPException(status_code = 403, detail = "Credenciales invalidos")
    order_product = await OrderProductService.create(db, upserts)
    if not order_product:
        raise HTTPException(status_code = 500, detail = "No se pudo añadir producto")
    return order_product