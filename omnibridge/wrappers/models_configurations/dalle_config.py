from .base_config import BaseConfiguration
from .config_types import ConfigTypes

class DALLEConfiguration(BaseConfiguration):
    def __init__(self, api_key: str, num_of_images: int, resolution: str) -> None:
        super().__init__(api_key)
        self.num_of_images = num_of_images
        self.resolution = resolution

    def _get_config_type() -> ConfigTypes:
        return ConfigTypes.DALLE