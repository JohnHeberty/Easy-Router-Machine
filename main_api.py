from fastapi import APIRouter, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from fastapi import FastAPI
import warnings

from src.adapters.controllers.login.login_controller import router as login_router
from src.adapters.controllers.docs.docs_controller import router as router_docs


warnings.filterwarnings('ignore')

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

main_router = APIRouter()

prefix_api = '/v0'
version = '0.1.0'


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@main_router.get("/", tags=['API Service'])
def read_root():
    headers = {"Custom-Header": "API APP DISBRAL"}
    return JSONResponse(content={"SERVICE ROUTER": "ONLINE","VERSAO DA API": version},
    status_code=200,
    headers=headers
)

@main_router.get("/openapi.json", tags=['Documentation'])
async def openapi():
    return get_openapi(title="API ROUTER", version=version, routes=app.routes)


app.include_router(main_router, prefix=prefix_api)

app.include_router(login_router, prefix=prefix_api)
app.include_router(router_docs, prefix=prefix_api)