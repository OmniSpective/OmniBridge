from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from omnibridge_api.app.core.config import settings
from omnibridge_api.app.api_v1.api import api_router

origins = [
    "http://localhost:3000",
    "localhost:3000"
]

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


app.include_router(api_router, prefix=settings.API_V1_STR)
