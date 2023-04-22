import json
from abc import ABC, abstractmethod
from typing import Optional

from omnibridge.model_entities.models_io.base_model_io import ModelIO, TextualIO


class PostprocessorBase(ABC):
    """A handler class for transforming output bytes from the
    SageMaker endpoint to a ModelIO.
    """

    """
    Example:
        .. code-block:: python
            class JSONPostprocessor(PostprocessorBase):
                accepts = "application/json"
                
                def transform_output(self, output: bytes) -> ModelIO:
                    response_json = json.loads(output.read().decode("utf-8"))
                    return TextualIO(response_json[0]["generated_text"])
    """
    accepts: Optional[str] = "text/plain"
    """The MIME type of the response data returned from endpoint"""

    @abstractmethod
    def transform_output(self, output: bytes) -> ModelIO:
        """Transforms the output from the model to string that
        the LLM class expects.
        """

    @classmethod
    @abstractmethod
    def get_name(cls) -> str:
        pass

class JsonToTextPostprocessor(PostprocessorBase):
    accepts = "application/json"
    
    def transform_output(self, output: bytes) -> ModelIO:
        response_json = json.loads(output.read().decode("utf-8"))
        return TextualIO(response_json[0]["generated_text"])

    @classmethod
    def get_name(cls) -> str:
        return 'TextPostprocessor'

MAP_POSTPROCESS_TYPE_TO_HANDLER = {
    JsonToTextPostprocessor.get_name(): JsonToTextPostprocessor
}