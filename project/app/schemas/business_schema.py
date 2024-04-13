from pydantic import BaseModel
from datetime import datetime
from typing import Union

class BusinessUpdate(BaseModel):
    name: Union[str, None] = None
    email: Union[str, None] = None
    password: Union[str, None] = None
    holder_id: Union[int, None] = None
    since: Union[datetime, None] = None
    class Config:
        orm_mode = True