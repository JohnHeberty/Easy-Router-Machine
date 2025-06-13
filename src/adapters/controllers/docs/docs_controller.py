from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBasic

security = HTTPBasic()
router = APIRouter()

prefix = '/v0' ## lembrar de trocar o prefixo

@router.get("/docs", tags=['Documentation'])
async def get_documentation():
    return get_swagger_ui_html(
        openapi_url=f"{prefix}/openapi.json",
        title="API PEX Docs"
    )

@router.get("/redoc", include_in_schema=False, tags=['Documentation'])
async def get_redoc_documentation():
    return get_redoc_html(openapi_url=f"{prefix}/openapi.json", title="API ReDoc Documentation")
