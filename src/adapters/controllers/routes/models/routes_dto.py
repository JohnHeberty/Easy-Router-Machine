from typing import Optional
from pydantic import BaseModel



class RoutesDTO(BaseModel):
    latitude_origem: str
    longitude_origem: str
    latitude_destino: str
    longitude_destino: str