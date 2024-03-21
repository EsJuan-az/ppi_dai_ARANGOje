from fastapi import Depends, APIRouter, HTTPException, Path, Query
from typing import Annotated
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.users import UserService
from ..schemas import UserCreate, UserUpdate, Login

router = APIRouter(prefix = "/user", tags = ['user'])

@router.get("/")
async def get_all(
    offset: Annotated[int, Query(title = "The page of user we want to get")] = 0,
    limit:  Annotated[int, Query(title = "The number of users we want to get per page")] = 10,
    db:Session = Depends(get_db),
    ):
    return UserService.get_all(db, offset, limit)

@router.get("/{id}")
async def get_by_id(
    id: Annotated[int, Path(title="ID of the user we want to find")],
    db: Session = Depends(get_db),
    ):
        user = UserService.get_by_id(db, id)
        if not user:
            raise HTTPException(status_code = 404, detail = "User not found")
        return user

@router.post("/", status_code = 201)
async def create(
    user:UserCreate,
    db: Session = Depends(get_db),
    ):
    new_user = UserService.create(db, user)
    if not new_user:
        raise HTTPException(status_code = 500, detail = "Couldn't create User")
    return new_user

@router.post('/auth')
async def login(
    login: Login,
    db: Session = Depends(get_db),
    ):
    user = UserService.login(db, login)
    if not user:
        raise HTTPException(status_code = 403, detail = "Invalid credentials")
    return user

@router.put("/")
async def update(
    user:UserUpdate,
    db: Session = Depends(get_db),
    ):
    new_user = UserService.update(db, user)
    if not new_user:
        raise HTTPException(status_code = 500, detail = "Couldn't update User")
    return new_user

@router.delete("/{id}")
async def delete(
    id: Annotated[int, Path(title="ID of the user we want to deactivate")],
    db: Session = Depends(get_db),
    ):
    new_user = UserService.delete(db, id)
    if not new_user:
        raise HTTPException(status_code = 500, detail = "Couldn't delete User")
    return new_user
