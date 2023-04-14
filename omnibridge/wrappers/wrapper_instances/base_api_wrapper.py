from typing import Any, Dict
import requests
from abc import ABC, abstractmethod
from ..wrapper_instance_configurations.base_config import BaseConfiguration
from ..wrapper_interfaces.textual_model_wrapper import TextualModelWrapper

import logging


class WrapperException(Exception):
    pass


class RestAPIWrapper(ABC):
    def __init__(self, configuration: BaseConfiguration, logger: logging.Logger = logging.getLogger()) -> None:
        self.config = configuration
        self.logger = logger

    def _get_headers(self) -> Dict[str, str]:
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config.api_key}"
        }

    @abstractmethod
    def _get_body(self, prompt_message: str) -> Any:
        pass

    @abstractmethod
    def _get_api_url(self) -> str:
        pass

    def prompt(self, prompt_message: str) -> Any:
        """
        raises GPTWrapperException if request failed
        returns string response from chatgpt completions api
        """
        self.logger.debug(f'Sending prompt to API: {prompt_message}')
        response = requests.post(
            self._get_api_url(),
            headers=self._get_headers(),
            data=self._get_body(prompt_message)
        )

        try:
            response.raise_for_status()
        except Exception as e:
            error_message = f"Request to api endpoint: {self._get_api_url()} failed.\n" \
                            f"Response message: {response.text}.\n" \
                            f"Exception caught: {e}"
            self.logger.error(error_message)
            raise WrapperException(error_message)

        return response.json()


class TextualRestAPIWrapper(RestAPIWrapper, TextualModelWrapper):
    @abstractmethod
    def _parse_response(self, response_json: Any) -> str:
        pass

    def prompt_and_get_response(self, prompt: str) -> str:
        return self._parse_response(self.prompt(prompt))
