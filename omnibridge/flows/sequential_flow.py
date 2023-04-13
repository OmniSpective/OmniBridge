from typing import List

from omnibridge.model_entities.base_model_entity import BaseModelUnit
from omnibridge.model_entities.models_io.base_model_io import ModelIO


class SequentialFlow:
    def __init__(self) -> None:
        self.models: List[BaseModelUnit] = []

    def is_valid_addition(self, new_model: BaseModelUnit) -> bool:
        if len(self.models) == 0:
            return True

        last_unit = self.models[-1]
        if new_model.can_process_type(last_unit.produced_type()):
            return True

        return False

    def add(self, new_model: BaseModelUnit) -> None:
        if not self.is_valid_addition(new_model):
            raise TypeError("Cannot add to this flow a model of this type.")

        self.models.append(new_model)

    def run_flow(self, flow_input: ModelIO) -> ModelIO:
        if len(self.models) == 0:
            raise RuntimeError("Cannot run empty flow.")

        if not self.models[0].can_process(flow_input):
            raise TypeError("Cannot run flow with input of this type.")

        model_input = flow_input
        for model in self.models:
            model_output = model.process(model_input)
            model_input = model_output

        return model_output
