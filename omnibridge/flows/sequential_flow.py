from typing import List, Dict, Union

from omnibridge.flows.flow import Flow
from omnibridge.model_entities.models_io.base_model_io import ModelIO
from omnibridge.wrappers.wrapper_instances.type_name_to_wrapper import ModelLoader
from omnibridge.wrappers.wrapper_interfaces.model_wrapper import ModelWrapper


class SequentialFlow(ModelWrapper, Flow):
    def __init__(self, name: str, models: Union[List[ModelWrapper], None] = None):
        self.name = name
        self.models = models or []

    def add(self, new_model: ModelWrapper, instruction: str) -> None:
        self.models.append(new_model)

    def process(self, model_input: ModelIO) -> ModelIO:
        if len(self.models) == 0:
            raise RuntimeError("Cannot run empty flow.")

        model_input = model_input
        for model in self.models:
            model_output = model.process(model_input)
            print(model_output)
            model_input = model_output

        return model_output

    def to_json(self) -> Dict[str, Union[str, int]]:
        return {
            '_class_type': self.get_class_type_field(),
            'models': ', '.join(model.get_name() for model in self.models)
        }

    @classmethod
    def create_from_json(cls, json_key, json_data: Dict[str, str]) -> Flow:
        name = json_key
        models_names = json_data['models'].split(', ')
        models = [ModelLoader.load_model(model_name) for model_name in models_names]
        return SequentialFlow(name, models)

    def get_name(self) -> str:
        return self.name

    @classmethod
    def get_class_type_field(cls) -> str:
        return "sequential"
