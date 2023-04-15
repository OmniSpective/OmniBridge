from enum import Enum
from typing import Dict, Any, Callable
from omnibridge.wrappers.api_key import ApiKey
from omnibridge.saved_data.json_data_manager import JsonDataManager
from omnibridge.wrappers.wrapper_instances.gpt_wrapper import GPTWrapper
from omnibridge.wrappers.wrapper_instances.dalle_wrapper import DALLEWrapper

from omnibridge.wrappers.wrapper_instances.type_name_to_wrapper import type_names

class Commands(str, Enum):
    ADD_KEY = "add-key"
    ADD_CHATGPT = "add-chatgpt"
    ADD_DALLE = "add-dalle"
    LIST_WRAPPERS = 'list-wrappers'


def add_key(args: Dict[str, Any], file_path: str = '') -> None:
    api_key = ApiKey(args['value'])
    JsonDataManager.save(["api keys", args['name']], api_key, file_path=file_path)


def add_chatgpt(args: Dict[str, Any], file_path: str = '') -> None:
    api_key: ApiKey = JsonDataManager.load(["api keys", args['key']], ApiKey, file_path=file_path)
    wrapper: GPTWrapper = GPTWrapper(api_key.value, args['model'])
    JsonDataManager.save(["models", args['name']], wrapper, file_path=file_path)


def add_dalle(args: Dict[str, Any], file_path: str = '') -> None:
    api_key: ApiKey = JsonDataManager.load(["api keys", args['key']], ApiKey, file_path=file_path)
    wrapper: DALLEWrapper = DALLEWrapper(api_key=api_key.value, number_of_images=args['num_images'],
                                            resolution=args['res'])
    JsonDataManager.save(["models", args['name']], wrapper, file_path=file_path)


def list_wrappers(args: Dict[str, Any], file_path: str = '') -> None:
    for type, wrapper in type_names.items():
        print (f'Wrapper: {type}')


COMMAND_TO_FUNCTION: Dict[str, Callable[[Dict[str, Any], str], None]] = {
    Commands.ADD_KEY: add_key,
    Commands.ADD_CHATGPT: add_chatgpt,
    Commands.ADD_DALLE: add_dalle,
    Commands.LIST_WRAPPERS: list_wrappers,
}