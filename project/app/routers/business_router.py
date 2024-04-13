from fastapi import Depends, APIRouter, HTTPException, Path, Query
from typing import Annotated
from sqlmodel import Session
from ..database import get_db
from ..models import Business
from ..services.business_service import BusinessService
from ..schemas.business_schema import BusinessUpdate
from ..schemas.login_schema import Login



router = APIRouter(prefix = "/business", tags = ['business'])

@router.get("/")
async def get_all(
    offset: Annotated[int, Query(title = "The page of business we want to get")] = 0,
    limit:  Annotated[int, Query(title = "The number of businesses we want to get per page")] = 10,
    db:Session = Depends(get_db),
    ):
    return await BusinessService.get_all(db, offset, limit)

@router.get("/{id}")
async def get_by_id(
    id: Annotated[int, Path(title="ID of the business we want to find")],
    db: Session = Depends(get_db),
    ):
        user = await BusinessService.get_by_id(db, id)
        if not user:
            raise HTTPException(status_code = 404, detail = "business not found")
        return user

@router.post("/", status_code = 201)
async def create(
    business:Business,
    db: Session = Depends(get_db),
    ):
    new_business = await BusinessService.create(db, business)
    if not new_business:
        raise HTTPException(status_code = 500, detail = "couldn't create Business")
    return new_business

@router.post('/auth')
async def login(
    login: Login,
    db: Session = Depends(get_db),
    ):
    user = await BusinessService.login(db, login)
    if not user:
        raise HTTPException(status_code = 403, detail = "invalid credentials")
    return user

@router.put("/{id}")
async def update(
    id: Annotated[int, Path(title="ID of the business we want to update")],
    business:BusinessUpdate,
    db: Session = Depends(get_db),
    ):
    new_business = await BusinessService.update(db, business, id)
    if not new_business:
        raise HTTPException(status_code = 500, detail = "couldn't update Business")
    return new_business

@router.delete("/{id}")
async def delete(
    id: Annotated[int, Path(title="ID of the business we want to deactivate")],
    db: Session = Depends(get_db),
    ):
    new_business = await BusinessService.delete(db, id)
    if not new_business:
        raise HTTPException(status_code = 500, detail = "couldn't delete Business")
    return new_business