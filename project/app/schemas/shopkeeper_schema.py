from pydantic import BaseModel
from typing import Union


class ShopkeeperUpdate(BaseModel):
    name: Union[str, None]
    business_id: Union[int, None] = None
    user_id: Union[int, None] = None
    class Config:
        orm_mode = True