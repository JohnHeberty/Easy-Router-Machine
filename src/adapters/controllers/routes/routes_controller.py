from fastapi import APIRouter, Depends, HTTPException
from typing import Dict

from src.adapters.controllers.routes.models.routes_dto_response import RoutesResponseDTO
from src.adapters.controllers.routes.models.routes_dto import RoutesDTO
from src.adapters.controllers.routes.routes_depends import get_routes_use_case
from src.app.use_case.routes.routes_use_case import RoutesUserCase
from src.domain.authorization.request_api import verify_request
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/routes/", response_model=RoutesResponseDTO, tags=['router'], response_model_exclude_none=True)  
async def routes(router: RoutesDTO, data: RoutesUserCase =  Depends(get_routes_use_case), authorization = Depends(verify_request)) -> Dict:
    try:
        response = data.execute(router.latitude_origem, router.longitude_origem, router.latitude_destino, router.longitude_destino)
        return RoutesResponseDTO(**response)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"STATUS": False, "DADOS": [], "ERRO": str(e)}
)