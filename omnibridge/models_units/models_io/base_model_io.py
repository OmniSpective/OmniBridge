from abc import ABC


class ModelIO(ABC):
    pass


class TextualIO(ModelIO):
    def __init__(self, text: str):
        self.text = text

    def get_text(self) -> str:
        return self.text


class FileIO(ModelIO):
    pass
