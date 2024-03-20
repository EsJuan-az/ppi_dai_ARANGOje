from pydantic import BaseModel
from datetime import datetime
from typing import Union

# BUSINESS: 
class BusinessBase(BaseModel):
    name: str
    email: str
    password: str
    holder_id: int
    class Config:
        orm_mode = True

class BusinessCreate(BusinessBase):
    pass    

class BusinessRead(BusinessBase):
    id: int
    since: Union[datetime, None] = None

class BusinessUpdate(BusinessBase):
    id: int
    name: Union[str, None] = None
    email: Union[str, None] = None
    password: Union[str, None] = None
    holder_id: Union[int, None] = None
    since: Union[datetime, None] = None

# SHOPKEEPER:
class ShopkeeperBase(BaseModel):
    name: str
    business_id: int
    user_id: int
    class Config:
        orm_mode = True

class ShopkeeperCreate(ShopkeeperBase):
    pass

class ShopkeeperRead(ShopkeeperBase):
    id: int
    business: BusinessRead

class ShopkeeperUpdate(ShopkeeperBase):
    id: int
    name: Union[str, None]
    business_id: Union[int, None] = None
    user_id: Union[int, None] = None

# USER:
class UserBase(BaseModel):
    name: str
    nick: str
    email: str
    password: str
    phone: str
    class Config:
        orm_mode = True
        
class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    id: int
    shopkeepers: set[ShopkeeperRead]
    businesses: set[BusinessRead]
    
class UserUpdate(UserBase):
    id: int
    name: Union[str, None] = None
    nick: Union[str, None] = None
    email: Union[str, None] = None
    password: Union[str, None] = None
    phone: Union[str, None] = None


# PRODUCT:
class ProductBase(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    stock: int
    business_id: int
    class Config:
        orm_mode = True
    
class ProductCreate(ProductBase):
    pass
    
class ProductRead(ProductBase):
    business: BusinessRead
    
class ProductUpdate(ProductBase):
    id: int
    name: Union[str, None] = None
    description: Union[str, None] = None
    price: Union[float, None] = None
    stock: Union[int, None] = None
    business_id: Union[int, None] = None