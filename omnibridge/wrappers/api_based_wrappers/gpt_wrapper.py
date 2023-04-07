from typing import Literal, TypedDict, Dict
import requests
import json

from ..models_configurations.chatgpt_config import GPTConfiguration, chatGptModel


COMPLETIONS_API_URL = "https://api.openai.com/v1/chat/completions"

class GPTWrapperException(Exception):
    pass

class CompletionsRequestBody(TypedDict):
    model: chatGptModel
    messages: list[dict[Literal["role", "content"], str]]


class GPTWrapper:
    def __init__(self, prompt: str, configuration: GPTConfiguration) -> None:
        self.prompt = prompt
        self.config = configuration

    def _get_headers(self) -> dict[str, str]:
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config.api_key}"
        }
    
    def _get_body(self) -> CompletionsRequestBody:
        return json.dumps({
            "model": self.config.model,
            "messages": [
                {"role": "user",
                 "content": self.prompt}
            ]
        })

    def __call__(self) -> Dict[str, str]:
        """
        raises GPTWrapperException if request failed
        returns string response from chatgpt completions api
        """
        response = requests.post(
            COMPLETIONS_API_URL,
            headers=self._get_headers(),
            data=self._get_body()
        )

        try:
            response.raise_for_status()
        except Exception as e:
            raise GPTWrapperException(f"Request to chatgpt completions api failed due to {e}. \n"
                                      f"Message response: {response.text}")
        
        return {'response': response.json()['choices'][0]['message']['content']}