from pydantic import BaseModel, ValidationError
from typing import Annotated, List, Union
class Login(BaseModel):
    email: str
    password: str
    scopes: list[str] = []
    grant_type: Union[str, None] = None
    client_id: Union[str, None] = None
    client_secret: Union[str, None] = None
    class Config:
        orm_mode = True