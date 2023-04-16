from typing import Dict, Any
from omnibridge.flows.branching_flow import BranchingFlow
from omnibridge.flows.sequential_flow import SequentialFlow
from omnibridge.wrappers.api_key import ApiKey
from omnibridge.saved_data.json_data_manager import JsonDataManager
from omnibridge.wrappers.wrapper_instances.gpt_wrapper import GPTWrapper
from omnibridge.wrappers.wrapper_instances.dalle_wrapper import DALLEWrapper
from omnibridge.wrappers.wrapper_instances.type_name_to_wrapper import ModelLoader


def add_key(args: Dict[str, Any]) -> None:
    api_key = ApiKey(args['value'])
    JsonDataManager.save(["api keys", args['name']], api_key, file_path=args['saved_data_file_path'])


def add_chatgpt(args: Dict[str, Any]) -> None:
    print(args)
    name = args['name']
    file_path = args['saved_data_file_path']
    api_key: ApiKey = JsonDataManager.load(["api keys", args['key']], ApiKey, file_path=file_path)
    wrapper: GPTWrapper = GPTWrapper(name, api_key.value, args['sub_model'])
    JsonDataManager.save(["models", name], wrapper, file_path=file_path)


def add_dalle(args: Dict[str, Any]) -> None:
    name = args['name']
    file_path = args['saved_data_file_path']
    api_key: ApiKey = JsonDataManager.load(["api keys", args['key']], ApiKey, file_path=file_path)
    wrapper: DALLEWrapper = DALLEWrapper(name, api_key=api_key.value, number_of_images=args['num_images'],
                                            resolution=args['res'])
    JsonDataManager.save(["models", name], wrapper, file_path=file_path)


def add_flow(args: Dict[str, Any]) -> None:
    file_path = args['saved_data_file_path']
    if args['type'] == 'branching':
            instructions = args['instruction']
            model = ModelLoader.load_model(args['model'])
            b_flow = BranchingFlow(args['name'], model, instructions)
            JsonDataManager.save(["flows", args["name"]], b_flow, file_path)
    elif args['type'] == 'seq':
        models = [ModelLoader.load_model(model_name) for model_name in args['multi']]
        flow = SequentialFlow(args['name'], models)
        JsonDataManager.save(["flows", args["name"]], flow, file_path)


MODEL_TYPE_TO_CREATION_FUNCTION = {
    'chatgpt': add_chatgpt,
    'dalle': add_dalle
}
