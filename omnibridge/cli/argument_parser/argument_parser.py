from omnibridge.cli.argument_parser.commands import Commands
from typing import Any

def add_api_key_arguments(parser: Any) -> Any:
    api_key_parser = parser.add_parser(Commands.ADD_KEY.value, help="Add an api key.")
    api_key_parser.add_argument('-n', '--name', help="name of the api key.", type=str, required=True)
    api_key_parser.add_argument('-v', '--value', help="value of the api key.", type=str, required=True)
    return api_key_parser


def add_chatgpt_arguments(parser: Any) -> Any:
    add_chatgpt_model_parser = parser.add_parser(Commands.ADD_CHATGPT.value, help="add chatgpt model connection details.")
    add_chatgpt_model_parser.add_argument('-n', '--name', type=str, required=True,
                                          help="name of the model, e.g. my_gpt4.")
    add_chatgpt_model_parser.add_argument('-k', '--key', type=str, required=True, help="api key name.")
    add_chatgpt_model_parser.add_argument('-m', '--model', type=str, default="gpt-3.5-turbo",
                                          help="model, e.g. 3.5 or 4.")
    return add_chatgpt_model_parser


def add_dalle_arguments(parser: Any) -> Any:
    add_dalle_model_parser = parser.add_parser(Commands.ADD_DALLE.value, help="add dalle model.")
    add_dalle_model_parser.add_argument('-n', '--name', type=str, required=True, help="name of the model.")
    add_dalle_model_parser.add_argument('-k', '--key', type=str, required=True, help="api key name.")
    add_dalle_model_parser.add_argument('--num-images', type=str, default="4",
                                          help="number of images per prompt, default 4.")
    add_dalle_model_parser.add_argument('-r', '--res', type=str, default="256x256", help="resolution of images.")
    return add_dalle_model_parser
