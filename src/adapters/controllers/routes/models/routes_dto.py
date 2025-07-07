from typing import Optional
from pydantic import BaseModel
from pydantic import Field


class RoutesDTO(BaseModel):
    latitude_origem: str = Field(..., example="-16.804450")
    longitude_origem: str = Field(..., example="-49.205938")
    latitude_destino: str = Field(..., example="-16.807019")
    longitude_destino: str = Field(..., example="-49.234030")


class InsertLocsDTO(BaseModel):
    nome_localizacao: str = Field(..., example="Posto do fulano")
    tipo: str = Field(..., example="Posto de combustíveis")
    latitude: str = Field(..., example="-16.804450")
    longitude: str = Field(..., example="-49.205938")

class UpdloadDfLocsDTO(BaseModel):
    coluna_tipo_localizacao: str = Field(..., example="tipo_localizacao")
    coluna_nome_localizacao: Optional[str] = Field(None, example="nome_localizacao")
    coluna_latitude: str = Field(..., example="latitude")
    coluna_longitude: str = Field(..., example="longitude")
    separador_csv: Optional[str] = Field(None, example=",", description="Separador do CSV, padrão é vírgula (',')")
    
