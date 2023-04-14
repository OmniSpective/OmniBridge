from fastapi import APIRouter
# from omnibridge.api.app.api_v1.endpoints import hello_world
from omnibridge_api.app.api_v1.endpoints import ai_models

api_router = APIRouter()
# api_router.include_router(hello_world.router, prefix="/hello", tags=["hello"])
api_router.include_router(ai_models.router, prefix="/ai_models", tags=["AI Models"])