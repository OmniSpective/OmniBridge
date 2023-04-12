from abc import abstractmethod, ABC


class TextualModelWrapper(ABC):
    @abstractmethod
    def prompt_and_get_response(self, prompt: str) -> str:
        pass
