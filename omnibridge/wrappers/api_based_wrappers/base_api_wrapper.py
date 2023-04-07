from typing import Any, Dict
import requests
from abc import ABC, abstractmethod
from ..models_configurations.base_config import BaseConfiguration

class WrapperException(Exception):
    pass


class RestAPIWrapper(ABC):
    def __init__(self, prompt: str, configuration: BaseConfiguration) -> None:
        self.prompt = prompt
        self.config = configuration

    def _get_headers(self) -> dict[str, str]:
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config.api_key}"
        }

    @abstractmethod
    def _get_body(self) -> Any:
        pass
    
    @abstractmethod
    def _get_api_url(self) -> str:
        pass

    @abstractmethod
    def _parse_response(self, response: Dict[str, Any]) -> str:
        pass

    def __call__(self) -> str:
        """
        raises GPTWrapperException if request failed
        returns string response from chatgpt completions api
        """
        response = requests.post(
            self._get_api_url(),
            headers=self._get_headers(),
            data=self._get_body()
        )

        try:
            response.raise_for_status()
        except Exception as e:
            raise WrapperException(f"Request to api endpoint failed due to {e}")
        
        return self._parse_response(response.json())