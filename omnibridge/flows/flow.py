from abc import abstractmethod, ABC

from omnibridge.wrappers.wrapper_interfaces.ModelWrapper import ModelWrapper


class Flow(ABC):
    @abstractmethod
    def add(self, new_model: ModelWrapper, instruction: str) -> None:
        pass
