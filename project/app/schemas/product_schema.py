from pydantic import BaseModel
from typing import Union


class ProductUpdate(BaseModel):
    name: Union[str, None] = None
    description: Union[str, None] = None
    price: Union[float, None] = None
    stock: Union[int, None] = None
    business_id: Union[int, None] = None
    class Config:
        orm_mode = True