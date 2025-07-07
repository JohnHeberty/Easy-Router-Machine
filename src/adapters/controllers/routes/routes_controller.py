from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from typing import Dict

from src.adapters.controllers.routes.models.routes_dto_response import RoutesResponseDTO
from src.adapters.controllers.routes.routes_depends import get_insert_loc_user_case
from src.adapters.controllers.routes.routes_depends import get_upload_locs_df_user_case
from src.adapters.controllers.routes.routes_depends import get_routes_use_case
from src.app.use_case.routes.insert_loc_use_case import InsertLocUserCase
from src.app.use_case.routes.upload_df_locs_use_case import UploadDfLocsUserCase
from src.adapters.controllers.routes.models.routes_dto import RoutesDTO, InsertLocsDTO, UpdloadDfLocsDTO
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
    
@router.post("/insert/loc-unique/", response_model=None, tags=['router'], response_model_exclude_none=True)  
async def routes(router: InsertLocsDTO, data: InsertLocUserCase =  Depends(get_insert_loc_user_case), authorization = Depends(verify_request)) -> Dict:
    try:
        response = data.execute(nome=router.nome_localizacao, 
                                tipo=router.tipo, 
                                latitude=router.latitude, 
                                longitude=router.longitude)
        return response
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"STATUS": False, "DADOS": [], "ERRO": str(e)}
)


@router.post("/upload-csv/")
async def upload_csv(
    coluna_tipo_localizacao: str = Form("tipo_localizacao", example="tipo_localizacao"),
    coluna_nome_localizacao: str = Form("nome_localizacao", example="nome_localizacao"),
    coluna_latitude: str = Form("latitude", example="latitude"),
    coluna_longitude: str = Form("longitude", example="longitude"),
    separador_csv: str = Form(";", example=";"),
    csv: UploadFile = File(..., description="Arquivo CSV com os dados"),
    data: UploadDfLocsUserCase = Depends(get_upload_locs_df_user_case)
):
    try:
        content = await csv.read()
        response = data.execute(
            nome_local=coluna_nome_localizacao,
            nome_coluna_tipo=coluna_tipo_localizacao,
            nome_coluna_latitude=coluna_latitude,
            nome_coluna_longitude=coluna_longitude,
            csv_content=content,
            separador_csv=separador_csv
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))