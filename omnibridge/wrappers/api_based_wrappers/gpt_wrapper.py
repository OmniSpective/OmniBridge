from typing import Literal, TypedDict, Dict, Any
import json

from .base_api_wrapper import RestAPIWrapper
from ..models_configurations.chatgpt_config import GPTConfiguration, chatGptModel

COMPLETIONS_API_URL = "https://api.openai.com/v1/chat/completions"


class GPTWrapperException(Exception):
    pass


class CompletionsRequestBody(TypedDict):
    model: chatGptModel
    messages: list[dict[Literal["role", "content"], str]]


class GPTWrapper(RestAPIWrapper):

    def __init__(self, configuration: GPTConfiguration) -> None:
        super().__init__(configuration)
        self.config = configuration
        self.api_url = COMPLETIONS_API_URL

    def _get_api_url(self) -> str:
        return self.api_url

    def _parse_response(self, response: Dict[str, Any]) -> Any:
        return {'response': response['choices'][0]['message']['content']}

    def _get_headers(self) -> dict[str, str]:
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config.api_key}"
        }

    def _get_body(self, prompt_message: str) -> CompletionsRequestBody:
        return json.dumps({
            "model": self.config.model,
            "messages": [
                {"role": "user",
                 "content": prompt_message}
            ]
        })
