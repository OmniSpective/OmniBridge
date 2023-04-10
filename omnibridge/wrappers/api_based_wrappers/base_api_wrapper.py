from typing import Any, Dict
import requests
from abc import ABC, abstractmethod
from ..models_configurations.base_config import BaseConfiguration


class WrapperException(Exception):
    pass


class RestAPIWrapper(ABC):
    def __init__(self, configuration: BaseConfiguration) -> None:
        self.config = configuration

    def _get_headers(self) -> dict[str, str]:
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

    @abstractmethod
    def _parse_response(self, response: Dict[str, Any]) -> Any:
        pass

    def prompt(self, prompt_message: str) -> Any:
        """
        raises GPTWrapperException if request failed
        returns string response from chatgpt completions api
        """
        response = requests.post(
            self._get_api_url(),
            headers=self._get_headers(),
            data=self._get_body(prompt_message)
        )

        try:
            response.raise_for_status()
        except Exception as e:
            raise WrapperException(f"Request to api endpoint: {self._get_api_url()} failed.\n"
                                   f"Response message: {response.text}.\n"
                                   f"Exception caught: {e}")
        
        return self._parse_response(response.json())
