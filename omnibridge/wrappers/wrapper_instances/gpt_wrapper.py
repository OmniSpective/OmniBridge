from typing import Dict, Any
import json

from .base_api_wrapper import TextualRestAPIWrapper
from ..wrapper_instance_configurations.chatgpt_config import GPTConfiguration
import logging

COMPLETIONS_API_URL = "https://api.openai.com/v1/chat/completions"


class GPTWrapper(TextualRestAPIWrapper):
    config: GPTConfiguration

    def __init__(self, configuration: GPTConfiguration, logger: logging.Logger=logging.getLogger()) -> None:
        super().__init__(configuration, logger)
        self.config = configuration
        self.api_url = COMPLETIONS_API_URL

    def _get_api_url(self) -> str:
        return self.api_url

    def _parse_response(self, response: Dict[str, Any]) -> Any:
        return {'response': response['choices'][0]['message']['content']}

    def _get_headers(self) -> Dict[str, str]:
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config.api_key}"
        }

    def _get_body(self, prompt_message: str) -> Any:
        return json.dumps({
            "model": self.config.model,
            "messages": [
                {"role": "user",
                 "content": prompt_message}
            ]
        })
