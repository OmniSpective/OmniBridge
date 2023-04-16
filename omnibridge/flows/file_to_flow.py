import json

from typing import Dict, Any

from .sequential_flow import SequentialFlow
from .branching_flow import BranchingFlow
from omnibridge.wrappers.wrapper_instances.type_name_to_wrapper import ModelLoader
from .flow import Flow

class FlowJsonParser:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self.flow: Flow | None = None

    def make_sequential(self) -> bool:
        """
        :return: bool - True if managed to create a sequential flow, o.w False
        """
        seq_models = []

        if len(self.models) != 1:
            return False

        model = self.models[0]

        while "models" in model:
            seq_models.append({"name": model["name"]})
            if len(model["models"]) != 1:
                return False
            
            model = model["models"][0]
        
        seq_models.append({"name": model["name"]})

        # Create Sequential Flow
        seq_models = [ModelLoader.load_model(item['name']) for item in seq_models]
        self.flow = SequentialFlow(name=self.name, models=seq_models)
        return True

    def make_branching(self) -> bool:
        """
        :return: bool - True if managed to create a branching flow, o.w False
        """
        if len(self.models) != 1:
            return False

        root_model = self.models[0]
        
        # Run over all "downstream" models, and verify that all of them do not 
        # have extra "models" and have "instruction" argument
        branch_instructions = []
        branch_models = []
        for idx, item in enumerate(root_model["models"]):
            if not(("instruction" in item) and ("models" not in item)):
                return False
            branch_models.append(ModelLoader.load_model(item["name"]))
            branch_instructions.append(item["instruction"])

        # Create Branching Flow
        self.flow =  BranchingFlow(name = self.name, 
                                    root_model=ModelLoader.load_model(root_model["name"]),
                                    branched_instructions=branch_instructions,
                                    branched_models=branch_models)
        return True

    def create_flow(self) -> None:
        if not(self.make_sequential() or self.make_branching()):
            raise Exception("Flow type is not supported")

    def unpack_json(self, json_data: Dict[Any, Any]) -> None:
        try:
            self.version = json_data['version']
            self.name = json_data['name']
            self.description = json_data['description']
            self.models = json_data['models']
        except Exception as e:
            raise Exception(f'JSON Scheme is wrong - {e}')

    def load(self) -> Flow:
        with open(self.file_path, 'r') as json_file:
            json_data = json.load(json_file)
        
        self.unpack_json(json_data=json_data)
        self.create_flow()
        
        return self.flow, self.name


