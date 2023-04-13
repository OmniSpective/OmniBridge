from typing import TypedDict, Any
import json
import requests
import logging
from .base_api_wrapper import RestAPIWrapper
from ..wrapper_instance_configurations.dalle_config import DALLEConfiguration
from ..wrapper_interfaces.file_generating_model_wrapper import FileGenModelWrapper

IMAGE_GENARATION_API_URL = "https://api.openai.com/v1/images/generations"


class ImageGenerationRequestBody(TypedDict):
    prompt: str
    n: int
    size: str


class DALLEWrapper(RestAPIWrapper, FileGenModelWrapper):
    config: DALLEConfiguration
    
    def __init__(self, configuration: DALLEConfiguration, logger: logging.Logger=logging.getLogger()) -> None:
        super().__init__(configuration, logger)
        self.api_url = IMAGE_GENARATION_API_URL
    
    def _get_body(self, prompt_message: str) -> Any:
        return json.dumps({
            "prompt": prompt_message,
            "n": self.config.num_of_images,
            "size": self.config.resolution
        })

    def _get_api_url(self) -> str:
        return self.api_url

    def prompt_and_generate_files(self, prompt: str) -> Any:
        response = self.prompt(prompt)

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
