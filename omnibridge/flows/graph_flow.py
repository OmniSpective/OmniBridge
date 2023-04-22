from typing import List, Dict, Any, Union

from omnibridge.model_entities.models_io.base_model_io import ModelIO, TextualIO
from omnibridge.model_entities.models_io.flow_io import FlowIO
from omnibridge.saved_data.json_data_manager import JsonConvertable
from omnibridge.wrappers.wrapper_instances.type_name_to_wrapper import ModelLoader
from omnibridge.wrappers.wrapper_interfaces.processor import Processor


class Node(JsonConvertable, Processor):
    def __init__(self, model: Processor, instruction: str = "", next_nodes: List[Processor] = []):
        self.next_nodes = next_nodes
        self.model = model
        self.instruction = instruction

    def process(self, model_input: ModelIO) -> FlowIO:
        assert isinstance(model_input, TextualIO)
        model_input = TextualIO(f"{model_input.get_text()} \n{self.instruction}")
        model_output = self.model.process(model_input)
        aggregate_output = FlowIO(model_output)
        for next_model in self.next_nodes:
            next_model_output = next_model.process(model_output)
            aggregate_output += next_model_output

        return aggregate_output

    def to_json(self) -> Dict[str, Union[str, int]]:
        raise NotImplementedError()

    @classmethod
    def create_from_json(cls, json_key: str, json_data: Dict[str, str]) -> Any:
        model_name = json_data['name']
        model = ModelLoader.load_model(model_name)

        instruction = json_data.get('instruction', "")

        next_models = []
        for next_model_data in json_data.get('models', []):
            next_model = Node.create_from_json("", next_model_data)  # type: ignore[arg-type]
            next_models.append(next_model)

        return Node(model, instruction, next_models)


class GraphFlow(JsonConvertable):
    def __init__(self, nodes: List[Node]):
        self.nodes = nodes

    def process(self, model_input: ModelIO) -> FlowIO:
        if len(self.nodes) == 0:
            raise ValueError("Cannot run flow with zero models!")

        flow_output = self.nodes[0].process(model_input)
        for node in self.nodes[1:]:
            flow_output += node.process(model_input)

        return flow_output

    def to_json(self) -> Dict[str, Union[str, int]]:
        raise NotImplementedError()

    @classmethod
    def create_from_json(cls, json_key: str, json_data: Dict[str, str]) -> Any:
        models_json = json_data['models']
        nodes = []
        for child_data in models_json:
            node = Node.create_from_json("", child_data)  # type: ignore[arg-type]
            nodes.append(node)
        return GraphFlow(nodes)
