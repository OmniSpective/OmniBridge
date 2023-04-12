from typing import TypedDict, Any
import json
import logging
from .base_api_wrapper import RestAPIWrapper
from ..models_configurations.hugging_face_config import HuggingFaceConfiguration

HUGGING_FACE_BASE_URL = "https://api-inference.huggingface.co/models"


class HuggingFaceModelRequestBody(TypedDict):
    prompt: str
    n: int
    size: str


class HuggingFaceWrapper(RestAPIWrapper):
    def __init__(self, configuration: HuggingFaceConfiguration, logger: logging.Logger=logging.getLogger()) -> None:
        super().__init__(configuration, logger)
        self.api_url = HUGGING_FACE_BASE_URL

    def _get_body(self, prompt_message: str) -> Any:
        return json.dumps({
            "inputs": prompt_message,
        })

    def _get_api_url(self) -> str:
        return f"{self.api_url}/{self.config.model_id}"
