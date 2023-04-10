from typing import TypedDict, Dict, Any
import json
import requests
from .base_api_wrapper import RestAPIWrapper
from ..models_configurations.dalle_config import DALLEConfiguration

IMAGE_GENARATION_API_URL = "https://api.openai.com/v1/images/generations"


class ImageGenerationRequestBody(TypedDict):
    prompt: str
    n: int
    size: str


class DALLEWrapper(RestAPIWrapper):
    def __init__(self, configuration: DALLEConfiguration) -> None:
        super().__init__(configuration)
        self.api_url = IMAGE_GENARATION_API_URL
    
    def _get_body(self, prompt_message: str) -> ImageGenerationRequestBody:
        return json.dumps({
            "prompt": prompt_message,
            "n": self.config.num_of_images,
            "size": self.config.resolution
        })

    def _get_api_url(self) -> str:
        return self.api_url

    def _parse_response(self, response: Dict[str, Any]) -> Any:
        images = []
        images_path = []
        data = response['data']
    
        for idx, item in enumerate(data):
            response = requests.get(item['url'])
            images.append(response.content)
            
            with open(f"image_{idx}.jpg", "wb") as f:
                f.write(response.content)
            images_path.append(f"image_{idx}.jpg")

        return {'images': images,
                'images_path': images_path}
