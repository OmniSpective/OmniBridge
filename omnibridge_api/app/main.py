from fastapi import FastAPI
from omnibridge.api.app.core.config import settings
from omnibridge.api.app.api_v1.api import api_router


app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)


app.include_router(api_router, prefix=settings.API_V1_STR)
