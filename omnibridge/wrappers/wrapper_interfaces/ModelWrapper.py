from abc import abstractmethod

from omnibridge.model_entities.models_io.base_model_io import ModelIO
from omnibridge.saved_data.json_data_manager import JsonConvertable


class ModelWrapper(JsonConvertable):
    @abstractmethod
    def process(self, model_input: ModelIO) -> ModelIO:
        pass
