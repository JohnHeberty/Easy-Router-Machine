from fastapi import APIRouter, Depends, HTTPException
from typing import Dict

from src.adapters.controllers.routes.models.routes_dto_response import RoutesResponseDTO
from src.adapters.controllers.routes.models.routes_dto import RoutesDTO
from src.adapters.controllers.routes.routes_depends import get_routes_use_case
from src.app.use_case.routes.routes_use_case import RoutesUserCase

router = APIRouter()

@router.post("/routes/", response_model=RoutesResponseDTO, tags=['router'])  
async def routes(router: RoutesDTO, data: RoutesUserCase =  Depends(get_routes_use_case)) -> Dict:
    try:
        response = data.execute(router.latitude_origem, router.longitude_origem, router.latitude_destino, router.longitude_destino)
        return RoutesResponseDTO(**response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))