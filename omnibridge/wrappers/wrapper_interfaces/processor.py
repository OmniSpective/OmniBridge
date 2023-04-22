from abc import abstractmethod, ABC

from omnibridge.model_entities.models_io.base_model_io import ModelIO


class Processor(ABC):
    @abstractmethod
    def process(self, model_input: ModelIO) -> ModelIO:
        pass
