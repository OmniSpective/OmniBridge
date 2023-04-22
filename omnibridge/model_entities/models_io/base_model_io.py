from abc import ABC
from typing import List


class ModelIO(ABC):
    pass


class TextualIO(ModelIO):
    def __init__(self, text: str):
        self.text = text

    def get_text(self) -> str:
        return self.text

    def __repr__(self):  # type: ignore
        return self.get_text()


class ImageIO(ModelIO):
    def __init__(self, paths: List[str]):
        self.paths = paths

    def image_paths(self):  # type: ignore
        return self.paths

    def __repr__(self):  # type: ignore
        return f"image paths: {self.paths}"


class FileIO(ModelIO):
    pass
