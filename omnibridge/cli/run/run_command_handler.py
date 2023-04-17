from typing import Dict, Any
from omnibridge.flows.flow_loader import FlowLoader
from omnibridge.model_entities.models_io.base_model_io import TextualIO
from omnibridge.wrappers.wrapper_instances.type_name_to_wrapper import ModelLoader


def handle_run_command(args: Dict[str, Any]) -> None:
    if args['object_to_run'] == 'model':
        run_model(args)
    elif args['object_to_run'] == 'flow':
        run_flow(args)


def run_flow(args: Dict[str, Any]) -> None:
    flow = FlowLoader.load_flow(args['name'])
    flow_input = TextualIO(args['prompt'])
    flow_output = flow.process(flow_input)
    print(flow_output)


def run_model(args: Dict[str, Any]) -> None:
    wrapper = ModelLoader.load_model(model_name=args['name'])
    response = wrapper.process(TextualIO(args['prompt']))
    print(response)