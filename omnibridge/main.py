import argparse
from omnibridge.model_entities.models_io.base_model_io import TextualIO
from omnibridge.cli.banner import banner
from omnibridge.cli.create.create_parser import add_create_arguments
from omnibridge.cli.run.run_parser import add_run_flow_sub_parser
from omnibridge.cli.list.list_parser import add_list_arguments
from omnibridge.cli.create.create_command_handler import handle_create_command
from omnibridge.cli.run.run_command_handler import handle_run_flow_command
from omnibridge.cli.list.list_command_handler import handle_list_command
from omnibridge.wrappers.wrapper_instances.type_name_to_wrapper import ModelLoader


def run() -> int:
    parser = argparse.ArgumentParser(description='AI integration tool.')
    parser.add_argument('-p', '--prompt', help="prompt for model", type=str, default=[])
    parser.add_argument('-n', "--model-name", help="which model to use.")

    subparsers = parser.add_subparsers(help='sub-command help', dest='command')

    create_parser = subparsers.add_parser("create", help="Create models/keys/flows.")
    create_subparsers = create_parser.add_subparsers(help='create sub-command help', dest='object_to_create')

    list_parser = subparsers.add_parser("list", help="List keys/models/flows/wrappers")
    list_subparsers = list_parser.add_subparsers(help="list sub-command help", dest="object_to_list")

    add_create_arguments(create_subparsers)
    add_run_flow_sub_parser(subparsers)
    add_list_arguments(list_subparsers)
    
    args = vars(parser.parse_args())

    if args['command'] == 'create':
        handle_create_command(args)
    elif args['command'] == 'list':
        handle_list_command(args)
    elif args['command'] == 'run-flow':
        handle_run_flow_command(args)
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
