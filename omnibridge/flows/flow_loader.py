from typing import Type, Dict

from omnibridge.flows.branching_flow import BranchingFlow
from omnibridge.flows.sequential_flow import SequentialFlow
from omnibridge.saved_data.json_data_manager import JsonDataManager, JsonConvertable
from omnibridge.wrappers.wrapper_interfaces.model_wrapper import ModelWrapper

flow_type_names: Dict[str, Type[JsonConvertable]] = {
    SequentialFlow.get_class_type_field(): SequentialFlow,
    BranchingFlow.get_class_type_field(): BranchingFlow,
}


class FlowLoader:
    @staticmethod
    def load_flow(flow_name: str) -> ModelWrapper:
        class_type_name = JsonDataManager.get_json_value(["flows", flow_name, "_class_type"])
        flow_type: Type[JsonConvertable] = flow_type_names[class_type_name]
        flow = JsonDataManager.load(["flows", flow_name], flow_type)
        return flow
