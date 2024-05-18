from fastapi import Depends, APIRouter, HTTPException, Path, Query, status
from typing import Annotated, Optional
from sqlmodel import Session
from ..database import get_db
from ..models import Record
from ..services.record_service import RecordService
from ..helpers.security.security_helper import UserSecurityHelper
from ..models import User
# Aquí instancio el Router de record para manejar sus respectivas peticiones.
router = APIRouter(prefix = "/record", tags = ['record'])

@router.get("/")
async def get_all(
    offset: Annotated[int, Query(title = "The page of record we want to get")] = 0,
    limit:  Annotated[int, Query(title = "The number of records we want to get per page")] = 30,
    db:Session = Depends(get_db),
    ):
    """Get all: Invoca al servicio para obtener todos los negocios.

    Args:
        offset (Annotated[int, Query, optional): Número de página. Defaults to "The page of business we want to get")]=0.
        limit (Annotated[int, Query, optional): Cantidad por página. Defaults to "The number of businesses we want to get per page")]=10.
        db (Session, optional): Motor de base de datos. Defaults to Depends(get_db).

    Returns:
        dict: Respuesta del servicio.
    """
    records = await RecordService.get_all(db, offset, limit)
    return [{**record.__dict__, "message": record.message} for record in records]