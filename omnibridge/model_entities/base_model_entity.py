from abc import ABC, abstractmethod
from typing import Any, Type

from omnibridge.model_entities.models_io.base_model_io import ModelIO


class BaseModelUnit(ABC):
    def can_process(self, model_input: ModelIO) -> bool:
        return self.can_process_type(type(model_input))

    @abstractmethod
    def can_process_type(self, model_input_type: Type[ModelIO]) -> bool:
        pass

    @abstractmethod
    def produced_type(self) -> Any:
        pass

    @abstractmethod
    def process(self, model_input: ModelIO) -> ModelIO:
        pass

