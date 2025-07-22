from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
import logging

from src.config import get_settings
from src.routers.blink1 import router as blink1_router
from src.helpers import setup_logs

app = FastAPI()
setup_logs("servant")
settings = get_settings()

app.include_router(blink1_router, prefix="/blink")


@app.get("/health")
async def health_check():
    return {"status": "ok"}


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Servant API",
        version="1.0.0",
        description="API server for controlling devices",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "HTTPBasic": {
            "type": "http",
            "scheme": "basic"
        }
    }
    
    for path, path_item in openapi_schema["paths"].items():
        if path.startswith("/blink"):
            for method, operation in path_item.items():
                if isinstance(operation, dict) and "operationId" in operation:
                    operation["security"] = [{"HTTPBasic": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

logging.info("servant started")
