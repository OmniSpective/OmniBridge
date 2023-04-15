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


class FlowTextIO(TextualIO):
    def __init__(self, text: str):
        super().__init__(text)
        self.pretty_text = text

    def __repr__(self) -> str:
        return self.pretty_text

    def __iadd__(self, other):  # type: ignore
        if isinstance(other, TextualIO):
            self.text += '\n' + other.get_text()
            self.pretty_text += '\n\n' + ('*' * 100) + '\n\n' + other.get_text()
            return self

        else:
            raise TypeError(f"unsupported operand type(s) for +: '{type(self).__name__}' and '{type(other).__name__}'")


class ImageIO(ModelIO):
    def __init__(self, paths: List[str]):
        self.paths = paths

    def image_paths(self):  # type: ignore
        return self.paths

    def __repr__(self):  # type: ignore
        return f"image paths: {self.paths}"

class FileIO(ModelIO):
    pass
