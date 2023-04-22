from typing import Any


def add_run_arguments(parser: Any) -> None:
    add_run_flow_sub_parser(parser)
    add_run_model_sub_parser(parser)


def add_run_flow_sub_parser(parser: Any) -> None:
    run_flow_parser = parser.add_parser("flow", help="run flow.")
    group = run_flow_parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-n', '--name', type=str, help="name of the flow.")
    group.add_argument('-f', '--file', type=str, help="name of json file containing a flow definition.")
    run_flow_parser.add_argument('-p', '--prompt', help="prompt for flow", type=str, required=True)


def add_run_model_sub_parser(parser: Any) -> None:
    run_flow_parser = parser.add_parser("model", help="run flow.")
    run_flow_parser.add_argument('-n', '--name', type=str, required=True, help="name of the flow.")
    run_flow_parser.add_argument('-p', '--prompt', help="prompt for flow", type=str, required=True)