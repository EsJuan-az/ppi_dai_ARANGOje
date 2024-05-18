from sqlmodel import Field, SQLModel, Relationship, TIMESTAMP, text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import Column, String
from enum import Enum
from sqlalchemy import func
from datetime import datetime
from typing import List, Optional
class Base(SQLModel):
    """Template basica para modelos de base.

    Args:
        id: int. Identificador.
        active: Entidad activa o no.
        created_at: Fecha de creación.k
        updated_at: Fecha de actualización.
    """
    id: int = Field(primary_key = True)
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
    """Modelo completo de usuario.
    
    Args:
        id: int. Identificador del usuario.
        name: str. Nombre completo del usuario.
        email: str. Correo del usuario.
        password: str. Contraseña del usuario.
        phone: string. Telefoo celular del usuario.
        shopkeepers: Shopkeeper[]. Lista de lugares donde es trabajador.
        own_businesses: Business[]. Lista de negocios propios.
        image: string. URL de imagen del usuario.
        active: boolean. Usuaio activo o no.
    """
    name: str = Field(nullable = False)
    email: str = Field(nullable = False, unique = True)
    password: str = Field(nullable = False)
    phone: str = Field(nullable = False, unique = True)
    shopkeepers: List['Shopkeeper'] = Relationship(
        back_populates = 'user',
        sa_relationship_kwargs={'lazy': 'selectin'},
        )
    own_businesses: List['Business'] = Relationship(
        back_populates = 'holder',
        sa_relationship_kwargs={'lazy': 'selectin'},
        )
    orders: List['Order'] = Relationship(
        back_populates='customer',
        )
    records: List['Record'] = Relationship(
        back_populates = 'user',
        )
    image: Optional[str] = Field(nullable = True)
    
    @property
    def associated_business_ids(self) -> list:
        return [
            *(business.id for business in self.own_businesses),
            *(shopkeeper.business_id for shopkeeper in self.shopkeepers)
            ]
    def is_associated_with_business(self, business_id: int) -> bool:
        """Revisa si el usuario es empleado o propietario del negocio.

        Args:
            business_id (int): El ID del negocio a revisar.

        Returns:
            bool: True si el usuario está asociado al negocio, False de otra manera.
        """
        #Check if the user owns the business
        if any(business.id == business_id for business in self.own_businesses):
            return True
        
        # Check if the user is a shopkeeper in the business
        if any(shopkeeper.business_id == business_id for shopkeeper in self.shopkeepers):
            return True

        return False
    
    
class Shopkeeper(Base, table = True):
    """Modelo completo de tendero.
    
    Args:
        id: int. Identificador del tendero.
        business_id: int FK. Identificador del negocio.
        lon: float. Longitúd de la ubicación actual.
        lat: float. Latitúd de la ubicación actual.
        working: bool. Está actualmente trabajando/disponible.
        user_id: int FK. Identificador del usuario.
        rol_id: int FK. 
        user: User.
        business: Business.
        active: bool. Tendero activo o no.
    """
    business_id: int = Field(nullable = False, foreign_key = 'business.id')
    lon: float = Field(nullable = True)
    lat: float = Field(nullable = True)
    working: bool = Field(default = False)
    user_id: int = Field(nullable = False, foreign_key = 'user.id')
    business: 'Business' = Relationship(
        back_populates = 'shopkeepers',
        sa_relationship_kwargs={'lazy': 'selectin'},
        )
    user: 'User' = Relationship(
        back_populates = 'shopkeepers',
        sa_relationship_kwargs={'lazy': 'selectin'},
        )
    

class Record(Base, table = True):
    """Modelo completo de anotación.
    
    Args:
        id: int. Identificador del anotación.
        business_id: int FK. Identificador del negocio.
        user_id: int FK. Identificador del usuario.
        raw_message: string.
        user: User.
        business: Business.
        active: bool. anotación activo o no.
    """
    business_id: int = Field(nullable = True, foreign_key = 'business.id')
    raw_message: str = Field(nullable = False)
    user_id: int = Field(nullable = True, foreign_key = 'user.id')
    business: Optional['Business'] = Relationship(
        back_populates = 'records',
        sa_relationship_kwargs={'lazy': 'selectin'},
        )
    user: Optional['User'] = Relationship(
        back_populates = 'records',
        sa_relationship_kwargs={'lazy': 'selectin'},
        )
    @property
    def message(self):
        message = self.raw_message
        if self.user is not None:
            message = message.replace('$uname$', self.user.name)
        if self.business is not None:
            message = message.replace('$bname$', self.business.name)
        return message
                


class Business(Base, table = True):
    """Modelo completo de negocio.
    
    Args:
        id: int. Identificador del negocio.
        name: str. Nombre del negocio.
        holder_id: int. Identificador del propietario.
        holder: User. Relación del propietario.
        shopkeepers: Shopkeeper[]. Lista de trabajadores.
        products: Product[]. Lista de productos.
        image: str|None. URL Imagen.
        active: bool. Negocio activo o no.
    """
    name: str = Field(nullable = False)
    holder_id: int = Field(foreign_key='user.id', nullable = False)
    description: str = Field(nullable=True);
    holder: 'User' = Relationship(
        back_populates = 'own_businesses',
        sa_relationship_kwargs={'lazy': 'selectin'},
        )
    shopkeepers: 'Shopkeeper' = Relationship(
        back_populates = 'business',
        )
    records: List['Record'] = Relationship(
        back_populates = 'business',
        )
    image: Optional[str] = Field( nullable = True)
    products: List['Product'] = Relationship(
        back_populates = 'business',
        )
    orders: List['Order'] = Relationship(
        back_populates = 'business',
        )
    

class Product(Base, table = True):
    """Modelo completo de producto.
    
    Args:
        id: int. Identificador del producto.
        name: string. Nombre del producto.
        description: str | None. Descripción del producto.
        price: float. Precio.
        stock: int. Existencias.
        business_id: int FK. Identificador del negocio al que pertenece.
        business: Business. Negocio al que pertenece.
        purchases: list[PurchaseProduct]: Compras.
        orders: list[OrderProduct]: Ordenes.
        images: list[str]. Lista de URL de imagenes.
        active: bool. Negocio activo o no.
    """
    name: str = Field(nullable = False)
    description: str | None = Field(nullable = True)
    price: float = Field(default=0.0)
    stock: int = Field(nullable = False)
    business_id: int = Field(nullable = False, foreign_key = 'business.id')
    business: 'Business'  = Relationship(
        back_populates='products',
        sa_relationship_kwargs={'lazy': 'subquery'},
        )
    order_products: List['OrderProduct'] = Relationship(
        back_populates='product',
        )
    images: List[str] = Field(sa_type=ARRAY(String), default=[])
    

class OrderStatus(Enum):
    """Enumeración de posibles estados para mi orden.
    - Aceptado: La orden ya fue revisada y procede a realizarse.
    - Cancelado: La orden ya no procede.
    - En espera: La orden no ha sido revisada.
    - Realizada: La orden ya fue realizada.
    """
    ACEPTADO = "ACEPTADO"
    CANCELADO = "CANCELADO"
    EN_ESPERA = "EN ESPERA"
    REALIZADA = "REALIZADA"

class Order(Base, table = True):
    """Modelo completo de orden.

    Args:
        id: int. Identificador de la orden.
        customer_id: int. Identificador del cliente.
        business_id: int. Identificador del negocio.
        lon: float. Longitúd de la ubicación.
        lat: float. Latitúd de de la ubicación.
        total_price: float. Suma total de todos los precios.
        status: str. Estado de la orden.

    """
    customer_id: int = Field(foreign_key="user.id", nullable=False)
    business_id: int = Field(foreign_key="business.id", nullable=False)
    lon: float = Field(nullable = True)
    lat: float = Field(nullable = True)
    order_products: List["OrderProduct"] = Relationship(
        back_populates="order",
        sa_relationship_kwargs={'lazy': 'selectin'},
        )
    customer: 'User' = Relationship(
        back_populates='orders',
        sa_relationship_kwargs={'lazy': 'selectin'},
        )
    business: 'Business' = Relationship(
        back_populates="orders",
        sa_relationship_kwargs={'lazy': 'selectin'},
        )
    status: OrderStatus = Field(default = OrderStatus.EN_ESPERA)
    @property
    def total_price(self) -> float:
        
        return sum(op.product.price * op.amount for op in self.order_products)
    
    @property
    def products(self) -> list:
        return [{'amount': orderproduct.amount, 'product': orderproduct.product} for orderproduct in self.order_products]
    
class OrderProduct(SQLModel, table = True):
    """Modelo completo de relación orden-producto.

    Args:
        order_id: int. Identificador de orden.
        product_id: int. Identificador del producto.
        amount: int. Cantidad del producto.
        purchase: Order. Order.
        product: Product. Producto.
    """
    __tablename__: str = 'order_product'
    order_id: int = Field(foreign_key="order.id", primary_key=True)
    product_id: int = Field(foreign_key="product.id", primary_key=True)
    amount: int = Field(default=1)
    order: Order = Relationship(
        back_populates="order_products",
        sa_relationship_kwargs={'lazy': 'selectin'},

        )
    product: Product = Relationship(
        back_populates="order_products",
        sa_relationship_kwargs={'lazy': 'selectin'},

        )
    