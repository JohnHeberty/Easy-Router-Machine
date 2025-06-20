from typing import Optional
from pydantic import BaseModel
from pydantic import Field


class RoutesDTO(BaseModel):
    latitude_origem: str = Field(..., example="-16.804450")
    longitude_origem: str = Field(..., example="-49.205938")
    latitude_destino: str = Field(..., example="-16.807019")
    longitude_destino: str = Field(..., example="-49.234030")
