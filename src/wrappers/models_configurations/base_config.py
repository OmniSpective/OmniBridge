
from typing import Any
from pathlib import Path
import json
from abc import ABC, abstractmethod
from .config_types import ConfigTypes

class BaseConfiguration(ABC):
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__
    
    def save_to_file(self) -> Path:
        config_path = Path(__file__).parent / '.config'
        with open(config_path, 'w') as f:
            f.write(json.dumps(self.to_dict()))

        return config_path
    
    @abstractmethod
    def _get_config_type() -> ConfigTypes:
        pass
