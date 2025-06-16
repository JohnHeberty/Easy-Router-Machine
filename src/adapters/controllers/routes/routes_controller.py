from fastapi import APIRouter, Depends, HTTPException
from typing import Dict

from src.adapters.controllers.routes.routes_depends import *
from src.adapters.controllers.routes.models.routes_dto_response import RoutesResponseDTO
router = APIRouter()


@router.get("/routes/", response_model=RoutesResponseDTO, tags=['router'])  
async def filials(data: FilialUseCase =  Depends(get_filial_use_case)) -> Dict:
    try:
        response = data.execute()
        return RoutesResponseDTO(**response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
