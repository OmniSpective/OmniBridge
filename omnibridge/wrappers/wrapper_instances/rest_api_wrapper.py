import time
from typing import Any, Dict
import requests
from abc import abstractmethod
from ..wrapper_interfaces.model_wrapper import ModelWrapper

import logging


class WrapperException(Exception):
    pass


class RestAPIWrapper(ModelWrapper):
    def __init__(self, name: str, logger: logging.Logger = logging.getLogger()) -> None:
        self.logger = logger
        self.name = name

    def _get_headers(self) -> Dict[str, str]:
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._get_api_key()}"
        }

    @abstractmethod
    def _get_api_key(self) -> str:
        pass

    @abstractmethod
    def _get_body(self, prompt_message: str) -> Any:
        pass

    @abstractmethod
    def _get_api_url(self) -> str:
        pass

    def get_name(self) -> str:
        return self.name

    def prompt(self, prompt_message: str) -> Any:
        """
        raises GPTWrapperException if request failed
        returns string response from chatgpt completions api
        """
        retries = 2
        retry_delay = 30  # seconds
        for attempt in range(retries):
            self.logger.debug(f'Sending prompt to API: {prompt_message}')
            response = requests.post(
                self._get_api_url(),
                headers=self._get_headers(),
                data=self._get_body(prompt_message)
            )

            if response.status_code == 429:
                self.logger.warning(
                    f"429 error: Too Many Requests. Retrying in {retry_delay} seconds. Attempt {attempt + 1}.")
                time.sleep(retry_delay)
                continue
            else:
                break
        try:
            response.raise_for_status()
        except Exception as e:
            error_message = f"Request to api endpoint: {self._get_api_url()} failed.\n" \
                            f"Response message: {response.text}.\n" \
                            f"Exception caught: {e}"
            self.logger.error(error_message)
            raise WrapperException(error_message)

        return response.json()
