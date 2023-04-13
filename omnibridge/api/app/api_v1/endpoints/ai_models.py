from fastapi import APIRouter
from omnibridge.api.app.schemas.ai_model import AIModel
from pathlib import Path
from typing import Any, List
import json

router = APIRouter()

@router.get("/models", response_model=List[AIModel])
def get_models() -> Any:
    models_path = Path(__file__).parents[2] / 'data/ai_models_metadata.json'

    with open(models_path, 'r') as f:
        models = json.load(f)

    return models