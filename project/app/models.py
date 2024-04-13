from sqlmodel import Field, SQLModel, Relationship, TIMESTAMP, text
from sqlalchemy import func
from datetime import datetime

class Base(SQLModel):
    id: int = Field(primary_key = True)
    active: bool = Field(default = True)
    created_at: datetime = Field(
        sa_type = TIMESTAMP(timezone=True),
        sa_column_kwargs={
            "server_default": func.now(),
        }
    )
    updated_at: datetime = Field(
        sa_type = TIMESTAMP(timezone=True),
        sa_column_kwargs={
            "server_default": func.now(),
            "server_onupdate": func.now()
        }
    )


class User(Base, table = True):
    """
    USER:
    id: int.
    name: string.
    nick: string.
    email: string.
    password: string.
    phone: string.
    shopkeepers: Shopkeeper[].
    own_businesses: Business[].
    image: string.
    active: boolean.
    """
    name: str = Field(nullable = False)
    nick: str = Field(nullable = False)
    email: str = Field(nullable = False, unique = True)
    password: str = Field(nullable = False)
    phone: str = Field(nullable = False, unique = True)
    shopkeepers: list['Shopkeeper'] = Relationship(back_populates = 'user')
    own_businesses: list['Business'] = Relationship(back_populates = 'holder')
    image: str | None = Field(nullable = True)
    
class Shopkeeper(Base, table = True):
    """
    SHOPKEEPER:
    id: int.
    name: str.
    business_id: int FK.
    user_id: int FK.
    active: boolean.
    rol_id: int FK. 
    user: User.
    business: Business.
    """
    #TODO: ROL_ID.
    name: str = Field(nullable = False)
    business_id: int = Field(nullable = False, foreign_key = 'business.id')
    user_id: int = Field(nullable = False, foreign_key = 'user.id')
    business: 'Business' = Relationship(back_populates = 'shopkeepers')
    user: 'User' = Relationship(back_populates = 'shopkeepers')   


class Business(Base, table = True):
    """
    BUSINESS:
    id: int.
    name: string.
    email: string.
    phone: string.
    password: string.
    holder_id: int FK.
    holder: User.
    shopkeepers: Shopkeeper[].
    products: Product[].
    image: string.
    plans: FK. 
    """
    #TODO: PLAN RELATIONSHIP N-N. 
    name: str = Field(nullable = False)
    email: str = Field(nullable = False, unique = True)
    phone: str = Field(nullable = False, unique = True)
    password: str = Field( nullable = False)
    holder_id: int = Field(foreign_key='user.id', nullable = False)
    holder: 'User' = Relationship(back_populates = 'own_businesses')
    shopkeepers: 'Shopkeeper' = Relationship(back_populates = 'business')
    image: str | None = Field( nullable = True)
    products: list['Product'] = Relationship(back_populates = 'business')
    

class Product(Base, table = True):
    """
    PRODUCT:
    id: int.
    name: string.
    description: string.
    price: float.
    stock: int.
    business_id: int FK.
    business: Business.
    """
    name: str = Field(nullable = False)
    description: str | None = Field(nullable = True)
    price: float = Field(nullable = False)
    stock: int = Field(nullable = False)
    business_id: int = Field(nullable = False, foreign_key = 'business.id')
    business: 'Business'  = Relationship(back_populates='products')



