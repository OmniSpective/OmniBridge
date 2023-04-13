from typing import Type

from omnibridge.wrappers.wrapper_interfaces.file_generating_model_wrapper import FileGenModelWrapper

from omnibridge.model_entities.base_model_entity import BaseModelUnit
from omnibridge.model_entities.models_io.base_model_io import ModelIO
from omnibridge.model_entities.models_io.base_model_io import TextualIO, FileIO


class ImageGenModel(BaseModelUnit):
    def __init__(self, image_gen_model_wrapper: FileGenModelWrapper):
        self.wrapper = image_gen_model_wrapper

    def can_process_type(self, model_input_type: Type[ModelIO]) -> bool:
        return issubclass(model_input_type, TextualIO)

    def produced_type(self) -> Type[FileIO]:
        return FileIO

    def process(self, model_input: TextualIO) -> FileIO:  # type: ignore[override]
        if not self.can_process(model_input):
            raise Exception(f"Cannot process input of type: {type(model_input)}")

        prompt = model_input.get_text()
        response = self.wrapper.prompt_and_generate_files(prompt)
        return response  # type: ignore[no-any-return]
