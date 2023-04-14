from typing import TypedDict, Any, Dict
import json
import requests
import logging
from .base_api_wrapper import RestAPIWrapper
from ..wrapper_instance_configurations.dalle_config import DALLEConfiguration
from ..wrapper_interfaces.file_generating_model_wrapper import FileGenModelWrapper
from ...saved_data.json_data_manager import JsonConvertable

IMAGE_GENARATION_API_URL = "https://api.openai.com/v1/images/generations"


class ImageGenerationRequestBody(TypedDict):
    prompt: str
    n: int
    size: str


class DALLEWrapper(RestAPIWrapper, FileGenModelWrapper, JsonConvertable):
    config: DALLEConfiguration

    def __init__(self, api_key: str, number_of_images: int, resolution: str,
                 logger: logging.Logger = logging.getLogger()) -> None:
        super().__init__(None, logger)
        self.api_url = IMAGE_GENARATION_API_URL
        self.api_key = api_key
        self.number_of_images = number_of_images
        self.resolution = resolution

    def to_json(self) -> Dict[str, str]:
        return {
            "api key": self.api_key,
            "number of images per prompt": self.number_of_images,
            "resolution": self.resolution,
            "_class_type": self._get_class_type_field()
        }

    @classmethod
    def create_from_json(cls, json_data: Dict[str, str]):
        return DALLEWrapper(api_key=json_data["api key"],
                            number_of_images=int(json_data["number of images per prompt"]),
                            resolution=json_data["resolution"])

    @classmethod
    def _get_class_type_field(cls):
        return "dalle_wrapper"

    def _get_body(self, prompt_message: str) -> Any:
        return json.dumps({
            "prompt": prompt_message,
            "n": self.config.num_of_images,
            "size": self.config.resolution
        })

    def _get_api_url(self) -> str:
        return self.api_url

    def _get_api_key(self) -> str:
        return self.api_key

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
