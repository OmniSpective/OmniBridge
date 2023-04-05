from typing import Literal, TypeVar, TypedDict
import requests
import json

COMPLETIONS_API_URL = "https://api.openai.com/v1/chat/completions"
chatGptModel = TypeVar('chatGptModel', bound=Literal["gpt-4", "gpt-4-0314",
                                                      "gpt-4-32k", "gpt-4-32k-0314",
                                                        "gpt-3.5-turbo", "gpt-3.5-turbo-0301"])

class GPTWrapperException(Exception):
    pass

class GPTConfiguration:
    def __init__(self, api_key: str, model: chatGptModel) -> None:
        self.api_key = api_key
        self.model = model

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
                {"role": "user"},
                {"content": self.prompt}
            ]
        })

    def __call__(self) -> str:
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
            raise GPTWrapperException(f"Request to chatgpt completions api failed due to {e}")
        
        return response.json()['choices']['message']['content']