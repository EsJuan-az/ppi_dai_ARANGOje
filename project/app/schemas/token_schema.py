from pydantic import BaseModel, ValidationError
from typing import Annotated, List, Union

class Token(BaseModel):
    access_token: str
    token_type: str
    
    
class TokenData(BaseModel):
    id: Union[int, None] = None
    scopes: List[str] = []


