from typing import Dict, Any
from omnibridge.flows.flow_loader import FlowLoader
from omnibridge.model_entities.models_io.base_model_io import TextualIO
from omnibridge.model_entities.models_io.file_to_text_converter import FileInputHandler


def handle_run_flow_command(args: Dict[str, Any]):
    flow = FlowLoader.load_flow(args['name'])
    if args['prompt_from_file']:
        flow_input = FileInputHandler.convert_file(args['prompt_from_file'])
    else:
        flow_input = TextualIO(args['prompt'])
    flow_output = flow.process(flow_input)
    print(flow_output)
