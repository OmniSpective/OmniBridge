from typing import TypedDict, Dict, Any
import json
from .base_api_wrapper import RestAPIWrapper
from ..models_configurations.hugging_face_config import HuggingFaceConfiguration

HUGGING_FACE_BASE_URL = "https://api-inference.huggingface.co/models"


class HuggingFaceModelRequestBody(TypedDict):
    prompt: str
    n: int
    size: str


class HuggingFaceWrapper(RestAPIWrapper):
    def __init__(self, configuration: HuggingFaceConfiguration) -> None:
        super().__init__(configuration)
        self.api_url = HUGGING_FACE_BASE_URL

    def _get_body(self, prompt_message: str) -> HuggingFaceModelRequestBody:
        return json.dumps({
            "inputs": prompt_message,
        })

    def _get_api_url(self) -> str:
        return f"{self.api_url}/{self.config.model_id}"

    def _parse_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        return response
