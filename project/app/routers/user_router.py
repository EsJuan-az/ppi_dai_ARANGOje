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
    return await UserService.get_all(db, offset, limit)

@router.get("/{id}")
async def get_by_id(
    id: Annotated[int, Path(title="ID of the user we want to find")],
    db: Session = Depends(get_db),
    ):
        user = await UserService.get_by_id(db, id)
        if not user:
            raise HTTPException(status_code = 404, detail = "user not found")
        return user

@router.post("/", status_code = 201)
async def create(
    user:User,
    db: Session = Depends(get_db),
    ):
    new_user = await UserService.create(db, user)
    if not new_user:
        raise HTTPException(status_code = 500, detail = "couldn't create User")
    return new_user

@router.post('/auth')
async def login(
    login: Login,
    db: Session = Depends(get_db),
    ):
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
    new_user = await UserService.update(db, user, id)
    if not new_user:
        raise HTTPException(status_code = 500, detail = "couldn't update User")
    return new_user

@router.delete("/{id}")
async def delete(
    id: Annotated[int, Path(title="ID of the user we want to deactivate")],
    db: Session = Depends(get_db),
    ):
    new_user = await UserService.delete(db, id)
    if not new_user:
        raise HTTPException(status_code = 500, detail = "couldn't delete User")
    return new_user
