from typing import Literal, TypedDict, Dict, Any
import requests
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
        pass

    def _parse_response(self, response: Dict[str, Any]) -> str:
        pass

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

    def prompt(self, prompt_message: str) -> Any:
        """
        raises GPTWrapperException if request failed
        returns string response from chatgpt completions api
        """
        response = requests.post(
            self.api_url,
            headers=self._get_headers(),
            data=self._get_body(prompt_message)
        )

        try:
            response.raise_for_status()
        except Exception as e:
            raise GPTWrapperException(f"Request to chatgpt completions api failed due to {e}. \n"
                                      f"Message response: {response.text}")

        return {'response': response.json()['choices'][0]['message']['content']}
