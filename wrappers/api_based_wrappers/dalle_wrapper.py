from typing import TypedDict, Dict, Any
import json
import requests
from .base_api_wrapper import RestAPIWrapper
from wrappers.models_configurations.dalle_config import DALLEConfiguration

COMPLETIONS_API_URL = "https://api.openai.com/v1/images/generations"


class CompletionsRequestBody(TypedDict):
    prompt: str
    n: int
    size: str


class DALLEWrapper(RestAPIWrapper):
    def __init__(self, prompt: str, configuration: DALLEConfiguration) -> None:
        super().__init__(prompt, configuration)
        self.api_url = COMPLETIONS_API_URL
    
    def _get_body(self) -> CompletionsRequestBody:
        return json.dumps({
            "prompt": self.prompt,
            "n": self.config.num_of_images,
            "size": self.config.resolution
        })

    def _get_api_url(self) -> str:
        return self.api_url

    def _parse_response(self, response: Dict[str, Any]) -> str:
        images = []
        data = response['data']
    
        for idx, item in enumerate(data):
            response = requests.get(item['url'])
            images.append(response.content)
            with open(f"image_{idx}.jpg", "wb") as f:
                f.write(response.content)

        return images