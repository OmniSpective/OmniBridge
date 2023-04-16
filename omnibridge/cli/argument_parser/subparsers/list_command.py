from typing import Any


def add_list_wrappers_arguments(parser: Any) -> None:
    parser.add_parser("list-wrappers", help="list wrappers.")