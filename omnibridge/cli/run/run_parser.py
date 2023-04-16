from typing import Any


def add_run_flow_sub_parser(parser: Any) -> None:
    run_flow_parser = parser.add_parser("run-flow", help="run flow.")
    run_flow_parser.add_argument('-n', '--name', type=str, required=True, help="name of the flow.")
    run_flow_parser.add_argument('-p', '--prompt', help="prompt for flow", type=str, required=True)