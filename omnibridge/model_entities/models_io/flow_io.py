from typing import List

from omnibridge.model_entities.models_io.base_model_io import ModelIO, TextualIO, ImageIO


class FlowIO(ModelIO):
    def __init__(self, model_io: ModelIO):
        self.text = ""
        self.image_paths = []
        self.pretty_text = ""

        if isinstance(model_io, TextualIO):
            self.text = model_io.get_text()
            self.pretty_text = self.text

        elif isinstance(model_io, ImageIO):
            self.image_paths = model_io.image_paths()
            self.pretty_text = repr(model_io)

        else:
            raise NotImplementedError()

    def get_text(self) -> str:
        return self.text

    def get_pretty_text(self) -> str:
        return self.pretty_text

    def get_image_paths(self) -> List[str]:
        return self.image_paths

    def __repr__(self) -> str:
        return self.get_pretty_text()

    def __iadd__(self, other):  # type: ignore
        line_seperator = '\n\n' + ('*' * 100) + '\n\n'

        if isinstance(other, TextualIO):
            self.text += '\n' + other.get_text()
            self.pretty_text += line_seperator + other.get_text()
            return self

        elif isinstance(other, ImageIO):
            self.image_paths += other.image_paths()
            self.pretty_text += line_seperator + repr(other)
            return self

        elif isinstance(other, FlowIO):
            self.text += '\n' + other.get_text()
            self.image_paths += other.get_image_paths()
            self.pretty_text += line_seperator + other.get_pretty_text()
            return self

        else:
            raise TypeError(f"unsupported operand type(s) for +: '{type(self).__name__}' and '{type(other).__name__}'")

