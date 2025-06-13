from typing import Optional
from pydantic import BaseModel #type: ignore

class LoginResponseDTO(BaseModel):
    STATUS: str
    TOKEN: Optional[str] = None
    CAT_ACESS: Optional[str] = None

class RegisterResponseDTO(BaseModel):
    STATUS  : bool
    
class FilialResponseDTO(BaseModel):
    STATUS  : bool
    DADOS   : Optional[dict] = None
