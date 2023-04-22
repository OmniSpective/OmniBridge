from typing import List

from omnibridge.model_entities.models_io.base_model_io import ModelIO, TextualIO, ImageIO


class FlowIO(ModelIO):
    def __init__(self, model_io: ModelIO):
        self.text = ""
        self.image_paths = []
        self.pretty_text = ""
        self._text_outputs_processed = 0
        self._image_outputs_processed = 0

        if isinstance(model_io, TextualIO):
            self.text = model_io.get_text()
            self.pretty_text = self.text
            self._text_outputs_processed += 1

        elif isinstance(model_io, ImageIO):
            self.image_paths = model_io.image_paths()
            self.pretty_text = repr(model_io)
            self._image_outputs_processed += 1

        else:
            raise NotImplementedError()

    def get_text(self) -> str:
        return self.text

    def get_pretty_text(self) -> str:
        return self.pretty_text

    def get_image_paths(self) -> List[str]:
        return self.image_paths

    def get_inputs_aggregated_amount(self) -> int:
        return self._text_outputs_processed + self._image_outputs_processed

    def __repr__(self) -> str:
        return self.get_pretty_text()

    def __iadd__(self, other):  # type: ignore
        line_seperator = '\n\n' + ('*' * 100) + '\n\n'

        if isinstance(other, TextualIO):
            self.text += '\n' + other.get_text()
            self.pretty_text += line_seperator + other.get_text()
            self._text_outputs_processed += 1
            return self

        elif isinstance(other, ImageIO):
            self.image_paths += other.image_paths()
            self.pretty_text += line_seperator + repr(other)
            self._image_outputs_processed += 1
            return self

        elif isinstance(other, FlowIO):
            self.text += '\n' + other.get_text()
            self.image_paths += other.get_image_paths()
            self.pretty_text += line_seperator + other.get_pretty_text()
            self._image_outputs_processed += other._image_outputs_processed
            self._text_outputs_processed += other._text_outputs_processed
            return self

        else:
            raise TypeError(f"unsupported operand type(s) for +: '{type(self).__name__}' and '{type(other).__name__}'")

