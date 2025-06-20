from typing import Optional
from pydantic import BaseModel


class RoutesResponseDTO(BaseModel):
    STATUS  : bool
    DADOS   : Optional[dict] = None
    ERRO    : Optional[str] = None
