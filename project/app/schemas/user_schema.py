from pydantic import BaseModel
from typing import Union


class UserUpdate(BaseModel):
    name: Union[str, None] = None
    nick: Union[str, None] = None
    email: Union[str, None] = None
    password: Union[str, None] = None
    phone: Union[str, None] = None
    class Config:
        orm_mode = True
