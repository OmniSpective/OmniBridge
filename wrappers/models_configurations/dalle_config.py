from .base_config import BaseConfiguration
from .config_types import ConfigTypes

class DALLEConfiguration(BaseConfiguration):
    def __init__(self, api_key: str, images: int, resolution: str) -> None:
        super().__init__(api_key)
        self.config_type = ConfigTypes.DALLE 
        self.images = images
        self.resolution = resolution