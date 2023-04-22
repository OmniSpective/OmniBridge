import json
from abc import ABC, abstractmethod
from typing import Optional, Dict

from omnibridge.model_entities.models_io.base_model_io import ModelIO, TextualIO


class PreprocessorBase(ABC):
    """A handler class to transform ModelIO to a
    format that SageMaker endpoint expects
    """

    """
    Example:
        .. code-block:: python
            class JSONPreprocessor(PreprocessorBase):
                content_type = "application/json"
                accepts = "application/json"
                def transform_input(self, prompt: ModelIO, model_kwargs: Dict) -> bytes:
                    if isinstance(prompt, TextualIO):
                        input_str = json.dumps({prompt:  prompt.text, **model_kwargs})
                    else:
                        raise Exception(f"{type(prompt) not supported as input"})
                    
                    return input_str.encode('utf-8')
    """

    content_type: Optional[str] = "text/plain"
    """The MIME type of the input data passed to endpoint"""

    @abstractmethod
    def transform_input(
        self, prompt: ModelIO, model_kwargs: Dict
    ) -> bytes:
        """Transforms the input ModelIO to a format that model can accept
        as the request Body. Should return bytes or seekable file
        like object in the format specified in the content_type
        request header.
        """
    @classmethod
    @abstractmethod
    def get_name(cls) -> str:
        pass


class TextToJSONPreprocessor(PreprocessorBase):
    content_type = "application/json"
    accepts = "application/json"
    def transform_input(self, prompt: ModelIO, model_kwargs: Dict) -> bytes:
        if isinstance(prompt, TextualIO):
            input_str = json.dumps({prompt:  prompt.text, **model_kwargs})
        else:
            raise Exception(f"{type(prompt)} not supported as input")
        
        return input_str.encode('utf-8')

    @classmethod
    def get_name(cls) -> str:
        return 'TextToJSONPreprocessor'

MAP_PREPROCESS_TYPE_TO_HANDLER = {
    TextToJSONPreprocessor.get_name(): TextToJSONPreprocessor
}

