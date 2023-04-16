from typing import Any


def add_list_arguments(parser: Any) -> None:
    add_list_flows_arguments(parser)
    add_list_keys_arguments(parser)
    add_list_models_arguments(parser)
    add_list_wrappers_arguments(parser)

def add_list_wrappers_arguments(parser: Any) -> None:
    parser.add_parser("wrappers", help="list supported wrappers")

def add_list_models_arguments(parser: Any) -> None:
    parser.add_parser("models", help="list existing models")

def add_list_keys_arguments(parser: Any) -> None:
    parser.add_parser("keys", help="list existing keys")

def add_list_flows_arguments(parser: Any) -> None:
    parser.add_parser("flows", help="list existing flows")
