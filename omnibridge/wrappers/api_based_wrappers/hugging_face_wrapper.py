from typing import TypedDict, Dict, Any
import json
from .base_api_wrapper import RestAPIWrapper
from ..models_configurations.hugging_face_config import HuggingFaceConfiguration

COMPLETIONS_API_URL = "https://api-inference.huggingface.co/models"

class GPTWrapperException(Exception):
    pass

class CompletionsRequestBody(TypedDict):
    prompt: str
    n: int
    size: str


class HuggingFaceWrapper(RestAPIWrapper):
    def __init__(self, prompt: str, configuration: HuggingFaceConfiguration) -> None:
        super().__init__(prompt, configuration)
        self.api_url = COMPLETIONS_API_URL
    
    def _get_body(self) -> CompletionsRequestBody:
        return json.dumps({
            "inputs": self.prompt,
        })

    def _get_api_url(self) -> str:
        return self.api_url + '/' + self.config.model_id

    def _parse_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        print (response)
        return response