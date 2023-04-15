from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from omnibridge_api.app.schemas.ai_model import AIModel, TextualModelPromptRequest, TextualModelPromptResponse
from pathlib import Path
from typing import List, Dict, Callable
import json

WRAPPER_TO_FUNC: Dict[str, Callable[[str, None], str]] = {} # TMP until cli implementation stabilizes

router = APIRouter()

@router.get("/models", response_model=List[AIModel], status_code=status.HTTP_200_OK)
def get_models() -> JSONResponse:
    models_path = Path(__file__).parents[2] / 'data/ai_models_metadata.json'

    try:
        with open(models_path, 'r') as f:
            models = json.load(f)
    except FileNotFoundError:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=[])

    return JSONResponse(status_code=status.HTTP_200_OK, content=models)


@router.post("/models/textual/prompts", response_model=TextualModelPromptResponse, status_code=status.HTTP_200_OK)
def prompt_textual_model(prompt_request: TextualModelPromptRequest) -> JSONResponse:
    model_name = prompt_request.model_name
    prompt = prompt_request.prompt

    wrapper_func = WRAPPER_TO_FUNC.get(model_name)

    if not wrapper_func:
        return JSONResponse(status_code=status.HTTP_501_NOT_IMPLEMENTED,
                             content={"response": f"{model_name} model is not supported"})


    return JSONResponse(status_code=status.HTTP_200_OK,
                         content={"response": wrapper_func(prompt, None)})
