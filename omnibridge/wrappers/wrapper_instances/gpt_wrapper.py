from typing import Dict, Any
import json

from .base_api_wrapper import TextualRestAPIWrapper
import logging

from ...saved_data.json_data_manager import JsonConvertable

COMPLETIONS_API_URL = "https://api.openai.com/v1/chat/completions"


class GPTWrapper(TextualRestAPIWrapper, JsonConvertable):
    def __init__(self, api_key: str, model: str, logger: logging.Logger=logging.getLogger()) -> None:
        if not api_key:
            raise ValueError("api key cannot be None.")
        if not model:
            raise ValueError("model cannot be None.")
        super().__init__(None, logger)
        self.api_url = COMPLETIONS_API_URL
        self.api_key = api_key
        self.model = model

    def to_json(self) -> Dict[str, str]:
        return {
            'api key': self.api_key,
            'model': self.model,
            '_class_type': self._get_class_type_field()
        }

    @classmethod
    def create_from_json(cls, json_data: Dict[str, str]):
        return GPTWrapper(json_data['api key'], json_data['model'])

    @classmethod
    def _get_class_type_field(cls): return "chat_gpt_wrapper"

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
