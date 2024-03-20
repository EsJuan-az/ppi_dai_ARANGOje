from sqlalchemy.orm import DeclarativeBase
from typing import Set
from sqlalchemy.sql import func
from sqlalchemy.types import TIMESTAMP, DateTime
from sqlalchemy import Boolean, String, Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    __mapper_args__ = {"eager_defaults": True}
    active: Mapped[bool] = mapped_column(Boolean(), default = True)
    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP(), server_default = func.now(), nullable = False)
    updated_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP(), server_default = func.now(), onupdate = func.now(), nullable = False)


class Business(Base):
    """BUSINESS:
    id: int
    name: string
    holder: int FK
    phone: string
    email: string
    password: string
    plan: int FK
    since: date"""
    __tablename__ = "business"
    id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column(String(), nullable = False)
    email: Mapped[str] = mapped_column(String(), nullable = False, unique = True)
    phone: Mapped[str] = mapped_column(String(), nullable = False, unique = True)
    password: Mapped[str] = mapped_column(String(), nullable = False)
    holder_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable = False)
    holder: Mapped["User"] = relationship(back_populates="businesses")
    shopkeepers: Mapped[Set['Shopkeeper']] = relationship(back_populates = "business")
    since: Mapped[DateTime] = mapped_column(DateTime(), nullable = True)
    products: Mapped[Set["Product"]] = relationship()
    

    def __repr__(self) -> str:
        return f"Business(id={self.id!r}, name={self.name!r}, email={self.email!r})"

class Product(Base):
    """PRODUCT:
    business_id: int FK
    name: string
    price: int
    stock: int
    description: string"""
    __tablename__ = "product"
    id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column(String(), nullable = False)
    description: Mapped[str] = mapped_column(String(), nullable = True)
    price: Mapped[float] = mapped_column(Float(), nullable = False)
    stock: Mapped[int] = mapped_column(Integer(), nullable = False)
    business_id: Mapped[int] = mapped_column(ForeignKey('business.id'), nullable = False)
    business: Mapped["Business"] = relationship(back_populates='products')
    def __repr__(self) -> str:
        return f"Product(id={self.id!r}, name={self.name!r}, price={self.price!r})"


class Shopkeeper(Base):
    """SHOPKEEPER:
    user_id: int
    business_id: int
    rol_id: int
    active: boolean"""
    __tablename__ = "shopkeeper"
    id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column(String(), nullable = False)
    business_id: Mapped[int] = mapped_column(ForeignKey('business.id'), nullable = False)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable = False)
    business: Mapped["Business"] = relationship(back_populates='shopkeepers')
    user: Mapped["User"] = relationship(back_populates='shopkeepers')
    # TODO: ROL ID.    

    def __repr__(self) -> str:
        return f"Shopkeeper(id={self.id!r}, business={self.business_id!r}, user={self.business_id!r})"


class User(Base):
    """USER:
    id: int
    name: string
    email: string
    password: string
    phone: string
    nick: string
    active: boolean"""
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(), nullable = False)
    nick: Mapped[str] = mapped_column(String(), nullable = False)
    email: Mapped[str] = mapped_column(String(), nullable = False, unique = True)
    password: Mapped[str] = mapped_column(String(), nullable = False)
    phone: Mapped[str] = mapped_column(String(), nullable = False, unique = True)
    shopkeepers: Mapped[Set['Shopkeeper']] = relationship(back_populates = "user")
    businesses: Mapped[Set["Business"]] = relationship(back_populates="holder")
    
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, email={self.email!r}, nickname={self.nick!r})"
