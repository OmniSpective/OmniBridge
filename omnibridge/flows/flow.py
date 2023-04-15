from abc import abstractmethod, ABC

from omnibridge.wrappers.wrapper_interfaces.model_wrapper import ModelWrapper


class Flow(ABC):
    @abstractmethod
    def add(self, new_model: ModelWrapper, instruction: str) -> None:
        pass
