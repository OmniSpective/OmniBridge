import argparse
import os
from omnibridge.model_entities.models_io.base_model_io import TextualIO
from omnibridge.cli.banner import banner
from omnibridge.cli.argument_parser.argument_parser import add_create_key_sub_parser, \
    add_create_model_sub_parser, add_create_flow_sub_parser, add_run_flow_sub_parser, \
    add_list_wrappers_arguments
from omnibridge.cli.argument_parser.command_handlers import handle_create_command, \
    handle_list_wrappers_command, handle_run_flow_command
from omnibridge.saved_data.json_data_manager import FILE_PATH

from omnibridge.wrappers.wrapper_instances.type_name_to_wrapper import ModelLoader

SAVED_DATA_FILE_PATH = os.getenv('SAVED_DATA_FILE_PATH', FILE_PATH)

def run() -> int:
    parser = argparse.ArgumentParser(description='AI integration tool.')
    parser.add_argument('-p', '--prompt', help="prompt for model", type=str, default=[])
    parser.add_argument('-n', "--model-name", help="which model to use.")

    subparsers = parser.add_subparsers(help='sub-command help', dest='command')
    create_parser = subparsers.add_parser("create", help="Create models/keys/flows.")
    create_subparsers = create_parser.add_subparsers(help='create sub-command help', dest='create_command')

    add_create_key_sub_parser(create_subparsers)
    add_create_model_sub_parser(create_subparsers)
    add_create_flow_sub_parser(create_subparsers)
    add_run_flow_sub_parser(subparsers)
    add_list_wrappers_arguments(subparsers)
    
    args = vars(parser.parse_args())

    if args['command'] == 'create':
        handle_create_command(args, SAVED_DATA_FILE_PATH)
    elif args['command'] == 'list-wrappers':
        handle_list_wrappers_command()
    elif args['command'] == 'run-flow':
        handle_run_flow_command(args, SAVED_DATA_FILE_PATH)

    elif args['prompt'] and args['model_name']:
        wrapper = ModelLoader.load_model(model_name=args['model_name'])
        response = wrapper.process(TextualIO(args['prompt']))
        print(response)
        return 0

    return 1


def main():
    print(banner)
    exit(run())


if __name__ == '__main__':
    main()
