from typing import TypedDict, Any, Dict, Union
import json
import requests
import logging
from .rest_api_wrapper import RestAPIWrapper
from ...model_entities.models_io.base_model_io import ModelIO, TextualIO, ImageIO

IMAGE_GENARATION_API_URL = "https://api.openai.com/v1/images/generations"


class ImageGenerationRequestBody(TypedDict):
    prompt: str
    n: int
    size: str


class DALLEWrapper(RestAPIWrapper):
    def __init__(self, name: str, api_key: str, number_of_images: int, resolution: str,
                 logger: logging.Logger = logging.getLogger()) -> None:
        super().__init__(name, logger)
        self.api_url = IMAGE_GENARATION_API_URL
        self.api_key = api_key
        self.number_of_images = number_of_images
        self.resolution = resolution

    def to_json(self) -> Dict[str, Union[str, int]]:
        return {
            "api key": self.api_key,
            "number of images per prompt": self.number_of_images,
            "resolution": self.resolution,
            "_class_type": self.get_class_type_field()
        }

    @classmethod
    def create_from_json(cls, json_key: str, json_data: Dict[str, str]) -> Any:
        return DALLEWrapper(json_key, api_key=json_data["api key"],
                            number_of_images=int(json_data["number of images per prompt"]),
                            resolution=json_data["resolution"])

    @classmethod
    def get_description(cls) -> str:
        return """
            DALLE-2 OpenAI Wrapper, generates an image based on text
        """

    @classmethod
    def get_class_type_field(cls) -> str:
        return "dalle"

    def _get_body(self, prompt_message: str) -> Any:
        return json.dumps({
            "prompt": prompt_message,
            "n": self.number_of_images,
            "size": self.resolution
        })

    def _get_api_url(self) -> str:
        return self.api_url

    def _get_api_key(self) -> str:
        return self.api_key

    def process(self, model_input: ModelIO) -> ImageIO:
        if not isinstance(model_input, TextualIO):
            raise TypeError(f"expected type {type(TextualIO)} but got {type(model_input)}")
        response = self.prompt(model_input.text)

        images = []
        images_path = []
        data = response['data']

        for idx, item in enumerate(data):
            response = requests.get(item['url'])
            images.append(response.content)

            with open(f"image_{idx}.jpg", "wb") as f:
                f.write(response.content)
            images_path.append(f"image_{idx}.jpg")

        return ImageIO(images_path)
