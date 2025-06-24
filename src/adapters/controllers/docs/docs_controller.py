from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from src.domain.authorization.request_api import verify_request
from src.app.helpers.api_functions import get_prefix_version
from fastapi.security import HTTPBasic
from fastapi import APIRouter, Depends

security = HTTPBasic()
router = APIRouter(dependencies=[Depends(security)])

prefix_api = get_prefix_version()

@router.get("/docs", tags=['Documentation'])
async def get_documentation(username: str = Depends(verify_request)):
    return get_swagger_ui_html(
        openapi_url=f"{prefix_api}/openapi.json",
        title="API PEX Docs"
)

@router.get("/redoc", include_in_schema=False, tags=['Documentation'])
async def get_redoc_documentation(username: str = Depends(verify_request)):
    return get_redoc_html(openapi_url=f"{prefix_api}/openapi.json", title="API ReDoc Documentation")
