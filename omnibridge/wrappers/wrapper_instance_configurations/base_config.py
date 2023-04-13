from __future__ import annotations
from typing import Any
from abc import ABC, abstractmethod
from .config_types import ConfigTypes


class BaseConfiguration(ABC):
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__

    @abstractmethod
    def _get_config_type(self) -> ConfigTypes:
        pass
