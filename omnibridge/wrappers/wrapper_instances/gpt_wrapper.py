from typing import Dict, Any, Union
import json

from .rest_api_wrapper import RestAPIWrapper
import logging

from ...model_entities.models_io.base_model_io import ModelIO, TextualIO

COMPLETIONS_API_URL = "https://api.openai.com/v1/chat/completions"


class GPTWrapper(RestAPIWrapper):
    def __init__(self, name: str, api_key: str, model: str = 'gpt-3.5-turbo',
                  logger: logging.Logger = logging.getLogger()) -> None:
        if not api_key:
            raise ValueError("api key cannot be None.")

        super().__init__(name, logger)
        self.api_url = COMPLETIONS_API_URL
        self.api_key = api_key
        self.model = model 

    def to_json(self) -> Dict[str, Union[str, int]]:
        return {
            'api key': self.api_key,
            'model': self.model,
            '_class_type': self.get_class_type_field()
        }

    @classmethod
    def create_from_json(cls, json_key: str, json_data: Dict[str, str]) -> Any:
        return GPTWrapper(json_key, json_data['api key'], json_data['model'])

    @classmethod
    def get_description(cls) -> str:
        return """
            ChatGPT OpenAI Wrapper, generates textual response given textual prompt.
            Can access different model versions.
        """

    @classmethod
    def get_class_type_field(cls) -> str:
        return "chat_gpt"

    def _get_api_url(self) -> str:
        return self.api_url

    def _parse_response(self, response: Dict[str, Any]) -> Any:
        return {'response': response['choices'][0]['message']['content']}

    def _get_api_key(self) -> str:
        return self.api_key

    def _get_body(self, prompt_message: str) -> Any:
        return json.dumps({
            "model": self.model,
            "messages": [
                {"role": "user",
                 "content": prompt_message}
            ]
        })

    def process(self, model_input: ModelIO) -> ModelIO:
        if not isinstance(model_input, TextualIO):
            raise TypeError(f"expected type {type(TextualIO)} but got {type(model_input)}")

        response = self.prompt(model_input.text)
        chat_answer = response['choices'][0]['message']['content']
        return TextualIO(chat_answer)
