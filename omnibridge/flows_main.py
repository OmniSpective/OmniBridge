from typing import Any

from omnibridge.flows.sequential_flow import SequentialFlow
from omnibridge.model_entities.textual_model_entity import TextualModel
from omnibridge.model_entities.image_gen_model_entity import ImageGenModel
from omnibridge.wrappers.wrapper_interfaces.textual_model_wrapper import TextualModelWrapper
from omnibridge.wrappers.wrapper_interfaces.file_generating_model_wrapper import FileGenModelWrapper
from omnibridge.model_entities.models_io.base_model_io import TextualIO


class MockedGPTWrapper(TextualModelWrapper):
    def prompt_and_get_response(self, prompt: str) -> str:
        return "mocked response"


class MockedDalleWrapper(FileGenModelWrapper):
    def prompt_and_generate_files(self, prompt: str) -> Any:
        return "mocked path of file"


if __name__ == '__main__':
    seq_flow = SequentialFlow()
    chatgpt_model = TextualModel(MockedGPTWrapper())
    dalle_model = ImageGenModel(MockedDalleWrapper())
    seq_flow.add(chatgpt_model)
    seq_flow.add(dalle_model)
    flow_input = TextualIO("flow input")
    result = seq_flow.run_flow(flow_input)
    print(result)
