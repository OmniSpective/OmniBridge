from typing import Type

from omnibridge.model_entities.base_model_entity import BaseModelUnit
from omnibridge.model_entities.models_io.base_model_io import ModelIO
from omnibridge.model_entities.models_io.base_model_io import TextualIO, ImageIO
from omnibridge.wrappers.wrapper_interfaces.model_wrapper import ModelWrapper


class TextToImageModel(BaseModelUnit):
    def __init__(self, textual_model_wrapper: ModelWrapper):
        self.wrapper = textual_model_wrapper

    def can_process_type(self, model_input_type: Type[ModelIO]) -> bool:
        return issubclass(model_input_type, TextualIO)

    def produced_type(self) -> Type[ImageIO]:
        return ImageIO

    def process(self, model_input: TextualIO) -> ImageIO:  # type: ignore
        if not self.can_process(model_input):
            raise Exception(f"Cannot process input of type: {type(model_input)}")

        prompt = model_input.get_text()
        response = self.wrapper.process(prompt=prompt)  # type: ignore
        image_output = ImageIO(response)  # type: ignore
        return image_output
