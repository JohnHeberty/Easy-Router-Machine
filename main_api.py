from fastapi import APIRouter, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from fastapi import FastAPI
import warnings

from src.adapters.controllers.docs.docs_controller import router as router_docs
from src.adapters.controllers.routes.routes_controller import router as routes_router
from src.app.helpers.api_functions import get_prefix_version, get_version
from src.infra.db.scripts.create_db import DatabaseInitializer

from src.adapters.task_service.task import TaskService

warnings.filterwarnings('ignore')

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

main_router = APIRouter()


version = get_version()
prefix_api = get_prefix_version()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    db_init = DatabaseInitializer()
    db_init.create_db_locales()


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
app.include_router(router_docs, prefix=prefix_api)
app.include_router(routes_router, prefix=prefix_api)

