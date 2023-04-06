from .base_config import BaseConfiguration
from .config_types import ConfigTypes

class HuggingFaceConfiguration(BaseConfiguration):
    def __init__(self, api_key: str, model_id: str) -> None:
        super().__init__(api_key)
        self.model_id = model_id

    def _get_config_type() -> ConfigTypes:
        return ConfigTypes.HUGGINGFACE