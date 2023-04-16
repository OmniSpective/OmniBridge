from omnibridge.common.supported_models import SupportedModels

from typing import Any


def add_create_model_sub_parser(parser: Any) -> None:
    create_model_parser = parser.add_parser("model", help="Create a new model.")
    create_model_parser.add_argument('model_type', choices=[m.value for m in SupportedModels], help="The type of model to create.")
    create_model_parser.add_argument('-n', '--name', type=str, required=True, help="name of the model.")
    create_model_parser.add_argument('-k', '--key', type=str, required=True, help="api key name.")
    create_model_parser.add_argument('--sub-model', type=str, help="the sub model of the model youv'e chosen, for example, 'gpt-3.5-turbo' if chatgpt is chosen")
    create_model_parser.add_argument('--num-images', type=str, default="4", help="number of images per prompt, default 4.")
    create_model_parser.add_argument('-r', '--res', type=str, default="256x256", help="resolution of images.")

def add_create_key_sub_parser(parser: Any) -> None:
    create_key_parser = parser.add_parser("key", help="Create an api key.")
    create_key_parser.add_argument('-n', '--name', help="name of the api key.", type=str, required=True)
    create_key_parser.add_argument('-v', '--value', help="value of the api key.", type=str, required=True)
