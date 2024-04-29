from pydantic import BaseModel
from typing import Union


class UserUpdate(BaseModel):
    """Esquema de actualización de Usuario en
    base de datos.

    Args:
        name (str|None): Nombre completo del usuario.
        email (str|None): Email del usuario.
        password (str|None): Contraseña del usuario.
        phone: (str|None): Telefono celular dle usuario.
    """
    name: Union[str, None] = None
    email: Union[str, None] = None
    password: Union[str, None] = None
    phone: Union[str, None] = None
    image: Union[str, None] = None
    class Config:
        orm_mode = True
