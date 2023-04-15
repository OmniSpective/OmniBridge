from abc import abstractmethod

from omnibridge.model_entities.models_io.base_model_io import ModelIO
from omnibridge.saved_data.json_data_manager import JsonConvertable


class ModelWrapper(JsonConvertable):
    @abstractmethod
    def process(self, model_input: ModelIO) -> ModelIO:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass

    @classmethod
    @abstractmethod
    def get_class_type_field(cls) -> str:
        pass
