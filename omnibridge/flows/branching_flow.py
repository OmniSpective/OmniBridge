from typing import Dict, List

from omnibridge.flows.flow import Flow
from omnibridge.model_entities.models_io.base_model_io import ModelIO, TextualIO
from omnibridge.wrappers.wrapper_instances.type_name_to_wrapper import ModelLoader
from omnibridge.wrappers.wrapper_interfaces.ModelWrapper import ModelWrapper


class BranchingFlow(ModelWrapper, Flow):
    def __init__(self, name: str, root_model: ModelWrapper, branched_models: List[ModelWrapper],
                 branched_instructions: List[str]):
        if len(branched_instructions) != len(branched_models):
            raise ValueError(f"Number of models and instructions must be the same.")
        self.name = name
        self.root_model = root_model
        self.branched_models = branched_models
        self.instructions = branched_instructions

    def process(self, model_input: ModelIO) -> ModelIO:
        root_output = self.root_model.process(model_input)
        assert isinstance(root_output, TextualIO)
        for model, instruction in zip(self.branched_models, self.instructions):
            model_input = TextualIO(root_output.text + " " + instruction)
            print(f"instruction: {instruction}")
            model_output = model.process(model_input)
            print(f"{model_output}")
            print('\n\n')
            print('*' * 100)

        return root_output  # TODO: merge the branches output to one output

    def get_name(self):
        return self.name

    @classmethod
    def get_class_type_field(cls):
        return "branching"

    def to_json(self) -> Dict[str, str]:
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
        return BranchingFlow(name, root_model, branched_models, branches_instruction)

    def add(self, new_model: ModelWrapper, instruction: str) -> None:
        self.branched_models.append(new_model)
        self.instructions.append(instruction)
