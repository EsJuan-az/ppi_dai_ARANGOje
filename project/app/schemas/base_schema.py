from pydantic import BaseModel
from datetime import datetime
from typing import Union

class Position(BaseModel):
    """Esquema de posición.
    
    Args:
        lon (float): Longitúd.
        lat (float): Latitúd.
    """
    lon: float
    lat: float