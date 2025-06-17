from typing import Optional
from pydantic import BaseModel



class RoutesDTO(BaseModel):
    latitude_inicio: str
    longitude_inicio: str
    latitude_fim: str
    longitude_fim: str