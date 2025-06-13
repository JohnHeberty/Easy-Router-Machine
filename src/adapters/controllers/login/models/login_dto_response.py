from typing import Optional
from pydantic import BaseModel #type: ignore


class FilialResponseDTO(BaseModel):
    STATUS  : bool
    DADOS   : Optional[dict] = None
