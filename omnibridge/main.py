import argparse
from omnibridge.model_entities.models_io.base_model_io import TextualIO
from omnibridge.cli.banner import banner
from omnibridge.cli.create.create_parser import add_create_key_sub_parser, \
    add_create_flow_sub_parser, add_create_model_sub_parser
from omnibridge.cli.run.run_parser import add_run_flow_sub_parser
from omnibridge.cli.list.list_parser import add_list_wrappers_arguments
from omnibridge.cli.create.create_command_handler import handle_create_command
from omnibridge.cli.run.run_command_handler import handle_run_flow_command
from omnibridge.cli.list.list_command_handler import handle_list_wrappers_command
from omnibridge.model_entities.models_io.file_to_text_converter import FileInputHandler
from omnibridge.wrappers.wrapper_instances.type_name_to_wrapper import ModelLoader


def run() -> int:
    parser = argparse.ArgumentParser(description='AI integration tool.')
    parser.add_argument('-n', "--model-name", help="which model to use.")
    input_params_group = parser.add_mutually_exclusive_group(required=True)
    input_params_group.add_argument('-p', '--prompt', help="prompt for model", type=str)
    input_params_group.add_argument("--prompt-from-file", type=str,
                                    help="provide file path to use its content as a prompt.")

    subparsers = parser.add_subparsers(help='sub-command help', dest='command')
    create_parser = subparsers.add_parser("create", help="Create models/keys/flows.")
    create_subparsers = create_parser.add_subparsers(help='create sub-command help', dest='object_to_create')

    add_create_key_sub_parser(create_subparsers)
    add_create_model_sub_parser(create_subparsers)
    add_create_flow_sub_parser(create_subparsers)
    add_run_flow_sub_parser(subparsers)
    add_list_wrappers_arguments(subparsers)

    args = vars(parser.parse_args())

    if args['command'] == 'create':
        handle_create_command(args)
    elif args['command'] == 'list-wrappers':
        handle_list_wrappers_command()
    elif args['command'] == 'run-flow':
        handle_run_flow_command(args)
    elif args['prompt'] and args['model_name']:
        wrapper = ModelLoader.load_model(model_name=args['model_name'])
        response = wrapper.process(TextualIO(args['prompt']))
        print(response)
    elif args['prompt_from_file'] and args['model_name']:
        wrapper = ModelLoader.load_model(model_name=args['model_name'])
        text_io = FileInputHandler.convert_file(args['prompt_from_file'])
        response = wrapper.process(text_io)
        print(response)
        return 0

    return 1


def main():
    print(banner)
    exit(run())


if __name__ == '__main__':
    main()
