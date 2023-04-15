from typing import Any, Dict, Union
import json
import logging

from .rest_api_wrapper import RestAPIWrapper
from ...model_entities.models_io.base_model_io import ModelIO, TextualIO

HUGGING_FACE_BASE_URL = "https://api-inference.huggingface.co/models"

class HuggingFaceWrapper(RestAPIWrapper):
    def __init__(self, name: str, api_key: str, model: str, logger: logging.Logger = logging.getLogger()) -> None:
        super().__init__(name, logger)
        self.api_url = HUGGING_FACE_BASE_URL
        self.api_key = api_key
        self.model = model

    def _get_api_key(self) -> str:
        return self.api_key

    def process(self, model_input: ModelIO) -> ModelIO:
        if isinstance(model_input, TextualIO):
            return TextualIO(self.prompt(prompt_message=model_input.text))
        else:
            raise NotImplementedError

    def to_json(self) -> Dict[str, Union[str, int]]:
        return {
            "api key": self.api_key,
            "model": self.model,
            "_class_type": self.get_class_type_field()
        }

    @classmethod
    def create_from_json(cls, json_key: str, json_data: Dict[str, str]) -> Any:
        return HuggingFaceWrapper(json_key, api_key=json_data["api key"], model=json_data["model"])

    @classmethod
    def get_description(cls) -> str:
        return """
            Huggin face wrapper, allow accessing any model in hugging face model that supports API endpoint
        """

    @classmethod
    def get_class_type_field(cls) -> str:
        return "hugging_face"

    def _get_body(self, prompt_message: str) -> Any:
        return json.dumps({
            "inputs": prompt_message,
        })

    def _get_api_url(self) -> str:
        return f"{self.api_url}/{self.model}"
