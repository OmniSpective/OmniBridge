from typing import Any, Dict, Union
import json
import logging

from .rest_api_wrapper import RestAPIWrapper
from ...model_entities.models_io.base_model_io import ModelIO, TextualIO

HUGGING_FACE_BASE_URL = "https://api-inference.huggingface.co/models"

SUPPORTED_TASKS = [
    "text2text-generation",
    "text-generation"
]


class HuggingFaceWrapper(RestAPIWrapper):
    def __init__(self, name: str, api_key: str, model: str, logger: logging.Logger = logging.getLogger()) -> None:
        """
        :param: model - hugging face repo
        """
        super().__init__(name, logger)
        self.api_url = HUGGING_FACE_BASE_URL
        self.api_key = api_key
        self.model = model

        from huggingface_hub import HfApi
        api = HfApi()
        model_info = api.model_info(repo_id=model)

        if model_info is None:
            raise Exception('Repo id do not exists')

        self.task = None
        for task in SUPPORTED_TASKS:
            if task in model_info.tags:
                self.task = task
                break

        if self.task is None:
            raise Exception('Task is not supported')

    def _get_api_key(self) -> str:
        return self.api_key

    def process(self, model_input: ModelIO) -> ModelIO:
        if not isinstance(model_input, TextualIO):
            raise NotImplementedError

        response = self.prompt(prompt_message=model_input.text)

        if "error" in response:
            raise ValueError(
                f"Error raised by inference API: {response['error']}"
            )

        if self.task == "text-generation":
            # Text response includes the prompt text.
            data = response[0]["generated_text"][len(model_input.text):]
        elif self.task == "text2text-generation":
            data = response[0]["generated_text"]
        else:
            raise Exception(f'Task {self.task} is not supported')

        return TextualIO(data)

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
            "inputs": prompt_message
        })

    def _get_api_url(self) -> str:
        return f"{self.api_url}/{self.model}"
