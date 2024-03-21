from fastapi import Depends, APIRouter, HTTPException, Path, Query
from typing import Annotated
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.business import BusinessService
from ..schemas import BusinessCreate, BusinessUpdate, Login



router = APIRouter(prefix = "/business", tags = ['business'])

@router.get("/")
async def get_all(
    offset: Annotated[int, Query(title = "The page of business we want to get")] = 0,
    limit:  Annotated[int, Query(title = "The number of businesses we want to get per page")] = 10,
    db:Session = Depends(get_db),
    ):
    return BusinessService.get_all(db, offset, limit)

@router.get("/{id}")
async def get_by_id(
    id: Annotated[int, Path(title="ID of the business we want to find")],
    db: Session = Depends(get_db),
    ):
        user = BusinessService.get_by_id(db, id)
        if not user:
            raise HTTPException(status_code = 404, detail = "Business not found")
        return user

@router.post("/", status_code = 201)
async def create(
    business:BusinessCreate,
    db: Session = Depends(get_db),
    ):
    new_business = BusinessService.create(db, business)
    if not new_business:
        raise HTTPException(status_code = 500, detail = "Couldn't create Business")
    return new_business

@router.post('/auth')
async def login(
    login: Login,
    db: Session = Depends(get_db),
    ):
    user = BusinessService.login(db, login)
    if not user:
        raise HTTPException(status_code = 403, detail = "Invalid credentials")
    return user

@router.put("/")
async def update(
    business:BusinessUpdate,
    db: Session = Depends(get_db),
    ):
    new_business = BusinessService.update(db, business)
    if not new_business:
        raise HTTPException(status_code = 500, detail = "Couldn't update Business")
    return new_business

@router.delete("/{id}")
async def delete(
    id: Annotated[int, Path(title="ID of the business we want to deactivate")],
    db: Session = Depends(get_db),
    ):
    new_business = BusinessService.delete(db, id)
    if not new_business:
        raise HTTPException(status_code = 500, detail = "Couldn't delete Business")
    return new_business