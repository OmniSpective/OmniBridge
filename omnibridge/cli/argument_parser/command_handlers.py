from typing import Dict, Any
from omnibridge.cli.argument_parser.commands import MODEL_TYPE_TO_CREATION_FUNCTION, add_flow, add_key
from omnibridge.flows.flow_loader import FlowLoader
from omnibridge.model_entities.models_io.base_model_io import TextualIO
from omnibridge.wrappers.wrapper_instances.type_name_to_wrapper import type_names


def handle_create_command(args: Dict[str, Any], saved_data_file_path: str):
    if args['create_command'] == 'model':
        creation_function = MODEL_TYPE_TO_CREATION_FUNCTION.get(args['model_type'])
        creation_function(args, saved_data_file_path)

    elif args['create_command'] == 'flow':
        add_flow(args, saved_data_file_path)

    elif args['create_command'] == 'key':
        add_key(args, saved_data_file_path)


def handle_list_wrappers_command():
    for type, _ in type_names.items():
        print (f'Wrapper: {type}')


def handle_run_flow_command(args: Dict[str, Any], saved_data_file_path: str):
    flow = FlowLoader.load_flow(args['name'], saved_data_file_path)
    flow_input = TextualIO(args['prompt'])
    flow_output = flow.process(flow_input)
    print(flow_output)