import os
import argparse
from omnibridge.model_entities.models_io.base_model_io import TextualIO
from omnibridge.saved_data.json_data_manager import JsonDataManager
from omnibridge.cli.banner import banner
from omnibridge.wrappers.wrapper_instances.type_name_to_wrapper import type_names
from omnibridge.cli.argument_parser.argument_parser import add_create_model_sub_parser, \
      add_create_key_sub_parser
from omnibridge.cli.argument_parser.commands import COMMAND_TO_FUNCTION
from omnibridge.saved_data.json_data_manager import FILE_PATH

SAVED_DATA_FILE_PATH = os.getenv("SAVED_DATE_FILE_PATH", FILE_PATH)


def run() -> int:
    parser = argparse.ArgumentParser(description='AI integration tool.')
    parser.add_argument('-p', '--prompt', help="prompt for model", type=str, default=[])
    parser.add_argument('-n', "--model-name", help="which model to use.")

    subparsers = parser.add_subparsers(help='sub-command help', dest='command')

    create_parser = subparsers.add_parser("create", help="Create models/keys")
    create_subparsers = create_parser.add_subparsers(help='Create models/keys', dest='create_command')

    add_create_model_sub_parser(create_subparsers)
    add_create_key_sub_parser(create_subparsers)

    args = vars(parser.parse_args())
    print(args)
    command_function = COMMAND_TO_FUNCTION.get(args['command'])
    if command_function:
        command_function(args, SAVED_DATA_FILE_PATH)
        return 0
    elif args['prompt'] and args['model_name']:
        class_type_name = JsonDataManager.get_json_value(["models", args['model_name'], "_class_type"])
        wrapper_type = type_names[class_type_name]
        wrapper = JsonDataManager.load(["models", args['model_name']], wrapper_type)  # type: ignore
        response = wrapper.process(TextualIO(args['prompt']))
        print(response)
        return 0

    return 1


def main() -> None:
    print(banner)
    exit(run())


if __name__ == '__main__':
    main()
