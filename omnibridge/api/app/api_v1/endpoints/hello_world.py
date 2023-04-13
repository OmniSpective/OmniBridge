from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def hello_world() -> dict[str, str]:
    return {"hello": "world"}