from typing import Dict, Any
from omnibridge.flows.flow_loader import FlowLoader
from omnibridge.model_entities.models_io.base_model_io import TextualIO
from omnibridge.wrappers.wrapper_instances.type_name_to_wrapper import ModelLoader


def handle_run_command(args: Dict[str, Any]) -> None:
    object_to_run = None
    if args['object_to_run'] == 'model':
        object_to_run = ModelLoader.load_model(model_name=args['name'])
    elif args['object_to_run'] == 'flow':
        object_to_run = FlowLoader.load_flow(args['name'])

    if not object_to_run:
        return
    
    response = object_to_run.process(TextualIO(args['prompt']))
    print(response)
