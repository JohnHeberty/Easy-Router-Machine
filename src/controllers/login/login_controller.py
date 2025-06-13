from fastapi import APIRouter, Depends, HTTPException # type: ignore
from typing import Dict

from src.adapters.controllers.login.models.login_dto_response import FilialResponseDTO
from src.app.use_case.login.filiais_use_case import FilialUseCase
from src.adapters.controllers.login.login_depends import *


router = APIRouter()

# EXEMPLO FILIAIS
@router.get("/FILIAIS/", response_model=FilialResponseDTO, tags=['Login'])  
async def filials(data: FilialUseCase =  Depends(get_filial_use_case)) -> Dict:
    try:
        response = data.execute()
        return FilialResponseDTO(**response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
