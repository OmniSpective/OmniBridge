from typing import Dict, List, Union

from omnibridge.flows.flow import Flow
from omnibridge.model_entities.models_io.base_model_io import ModelIO, TextualIO
from omnibridge.model_entities.models_io.flow_io import FlowIO
from omnibridge.saved_data.json_data_manager import JsonConvertable
from omnibridge.wrappers.wrapper_instances.type_name_to_wrapper import ModelLoader
from omnibridge.wrappers.wrapper_interfaces.model_wrapper import ModelWrapper


class BranchingFlow(Flow, JsonConvertable):
    def __init__(self, name: str, root_model: ModelWrapper, branched_instructions: List[str],
                 branched_models: Union[List[ModelWrapper], None] = None):
        if branched_models is None:
            self.branched_models = [root_model for _ in range(len(branched_instructions))]
        elif len(branched_instructions) != len(branched_models):
            raise ValueError("Number of models and instructions must be the same.")
        else:
            self.branched_models = branched_models
        self.name = name
        self.root_model = root_model
        self.instructions = branched_instructions

    def process(self, model_input: ModelIO) -> FlowIO:
        root_output = self.root_model.process(model_input)
        assert isinstance(root_output, TextualIO)
        flow_output = FlowIO(root_output)
        for model, instruction in zip(self.branched_models, self.instructions):
            model_input = TextualIO(root_output.get_text() + "\n" + instruction)
            model_output = model.process(model_input)
            flow_output += model_output

        return flow_output

    def get_name(self) -> str:
        return self.name

    @classmethod
    def get_class_type_field(cls):
        return "branching"

    def to_json(self) -> Dict[str, Union[str, int]]:
        return {
            '_class_type': self.get_class_type_field(),
            'root_model': self.root_model.get_name(),
            'branched_models': ', '.join(model.get_name() for model in self.branched_models),
            'instructions': '$$$'.join(instruction for instruction in self.instructions)
        }

    @classmethod
    def create_from_json(cls, json_key: str, json_data: Dict[str, str]):
        name = json_key
        root_model = ModelLoader.load_model(json_data['root_model'])
        branched_models_names = json_data['branched_models'].split(', ')
        branched_models = [ModelLoader.load_model(model_name) for model_name in branched_models_names]
        branches_instruction = json_data['instructions'].split('$$$')
        return BranchingFlow(name, root_model, branches_instruction, branched_models)

    def add(self, new_model: ModelWrapper, instruction: str) -> None:
        self.branched_models.append(new_model)
        self.instructions.append(instruction)
