from fastapi import Depends, APIRouter, HTTPException, Path, Query
from typing import Annotated
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.shopkeeper import ShopkeeperService
from ..schemas import ShopkeeperCreate, ShopkeeperUpdate

router = APIRouter(prefix = "/shopkeeper", tags = ['shopkeeper'])

@router.get("/")
async def get_all(
    offset: Annotated[int, Query(title = "The page of shopkeepers we want to get")] = 0,
    limit:  Annotated[int, Query(title = "The number of shopkeepers we want to get per page")] = 10,
    db:Session = Depends(get_db),
    ):
    return ShopkeeperService.get_all(db, offset, limit)

@router.get("/{id}")
async def get_by_id(
    id: Annotated[int, Path(title="ID of the product we want to find")],
    db: Session = Depends(get_db),
    ):
        shopkeeper = ShopkeeperService.get_by_id(db, id)
        if not shopkeeper:
            raise HTTPException(status_code = 404, detail = "shopkeeper not found")
        return shopkeeper

@router.post("/", status_code = 201)
async def create(
    shopkeeper:ShopkeeperCreate,
    db: Session = Depends(get_db),
    ):
    new_shopkeeper = ShopkeeperService.create(db, shopkeeper)
    if not new_shopkeeper:
        raise HTTPException(status_code = 500, detail = "couldn't create shopkeeper")
    return new_shopkeeper

@router.put("/")
async def update(
    shopkeeper:ShopkeeperUpdate,
    db: Session = Depends(get_db),
    ):
    new_shopkeeper = ShopkeeperService.update(db, shopkeeper)
    if not new_shopkeeper:
        raise HTTPException(status_code = 500, detail = "couldn't update shopkeeper")
    return new_shopkeeper

@router.delete("/{id}")
async def delete(
    id: Annotated[int, Path(title="ID of the shopkeeper we want to deactivate")],
    db: Session = Depends(get_db),
    ):
    new_shopkeeper = ShopkeeperService.delete(db, id)
    if not new_shopkeeper:
        raise HTTPException(status_code = 500, detail = "couldn't delete shopkeeper")
    return new_shopkeeper