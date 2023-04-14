from typing import Dict
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def hello_world() -> Dict[str, str]:
    return {"hello": "world"}