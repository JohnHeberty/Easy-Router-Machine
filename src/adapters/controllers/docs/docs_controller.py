from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBasic
from src.app.helpers.api_functions import get_prefix_version

security = HTTPBasic()
router = APIRouter()

prefix_api = get_prefix_version()

@router.get("/docs", tags=['Documentation'])
async def get_documentation():
    return get_swagger_ui_html(
        openapi_url=f"{prefix_api}/openapi.json",
        title="API PEX Docs"
)

@router.get("/redoc", include_in_schema=False, tags=['Documentation'])
async def get_redoc_documentation():
    return get_redoc_html(openapi_url=f"{prefix_api}/openapi.json", title="API ReDoc Documentation")
