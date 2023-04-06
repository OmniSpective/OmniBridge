from .base_config import BaseConfiguration
from .config_types import ConfigTypes
from typing import TypeVar, Literal

chatGptModel = TypeVar('chatGptModel', bound=Literal["gpt-4", "gpt-4-0314",
                                                      "gpt-4-32k", "gpt-4-32k-0314",
                                                        "gpt-3.5-turbo", "gpt-3.5-turbo-0301"])

class GPTConfiguration(BaseConfiguration):
    def __init__(self, api_key: str, model: chatGptModel) -> None:
        super().__init__(api_key)
        self.model = model

    def _get_config_type() -> ConfigTypes:
        return ConfigTypes.CHATGPT