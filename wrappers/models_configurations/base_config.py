
from typing import Any
from pathlib import Path
from .config_types import ConfigTypes
import json

class BaseConfiguration:
    def __init__(self, api_key: str) -> None:
        self.config_type = ConfigTypes.BASE
        self.api_key = api_key

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__
    
    def to_file(self) -> Path:
        config_path = Path(__file__).parent / f'.config_{self.config_type}'
        with open(config_path, 'w') as f:
            f.write(json.dumps(self.to_dict()))

        return config_path
