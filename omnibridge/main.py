import argparse

from omnibridge.cli.banner import banner
from omnibridge.cli.create.create_parser import add_create_arguments
from omnibridge.cli.run.run_parser import add_run_arguments
from omnibridge.cli.list.list_parser import add_list_arguments
from omnibridge.cli.create.create_command_handler import handle_create_command
from omnibridge.cli.run.run_command_handler import handle_run_command
from omnibridge.cli.list.list_command_handler import handle_list_command

COMMAND_TO_HANDLER = {
    'create': handle_create_command,
    'list': handle_list_command,
    'run': handle_run_command
}


def run() -> int:
    parser = argparse.ArgumentParser(description='AI integration tool.')
    subparsers = parser.add_subparsers(help='sub-command help', dest='command')

    create_parser = subparsers.add_parser("create", help="Create models/keys/flows.")
    create_subparsers = create_parser.add_subparsers(help='create sub-command help', dest='object_to_create')

    list_parser = subparsers.add_parser("list", help="List keys/models/flows/wrappers")
    list_subparsers = list_parser.add_subparsers(help="list sub-command help", dest="object_to_list")

    run_parser = subparsers.add_parser("run", help="Run model/flow")
    run_subparsers = run_parser.add_subparsers(help="run sub-command help", dest="object_to_run")

    add_create_arguments(create_subparsers)
    add_list_arguments(list_subparsers)
    add_run_arguments(run_subparsers)
    
    args = vars(parser.parse_args())

    handler = COMMAND_TO_HANDLER[args['command']]
    handler(args)

    return 0


def main():
    print(banner)
    exit(run())


if __name__ == '__main__':
    main()
