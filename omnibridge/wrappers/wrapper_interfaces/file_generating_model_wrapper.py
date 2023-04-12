from abc import abstractmethod, ABC
from typing import Any


class FileGenModelWrapper(ABC):
    @abstractmethod
    def prompt_and_generate_files(self, prompt: str) -> Any:
        pass
