from typing import Dict, Any
from omnibridge.flows.branching_flow import BranchingFlow
from omnibridge.flows.sequential_flow import SequentialFlow
from omnibridge.wrappers.api_key import ApiKey
from omnibridge.saved_data.json_data_manager import JsonDataManager
from omnibridge.wrappers.wrapper_instances.gpt_wrapper import GPTWrapper
from omnibridge.wrappers.wrapper_instances.dalle_wrapper import DALLEWrapper
from omnibridge.wrappers.wrapper_instances.hugging_face_wrappers import HuggingFaceWrapper
from omnibridge.wrappers.wrapper_instances.type_name_to_wrapper import ModelLoader


def handle_create_command(args: Dict[str, Any]) -> None:
    if args['object_to_create'] == 'model':
        creation_function = MODEL_TYPE_TO_CREATION_FUNCTION.get(args['model_type'])
        if not creation_function:
            print('model type is not supported')
            return
        creation_function(args)

    elif args['object_to_create'] == 'flow':
        add_flow(args)

    elif args['object_to_create'] == 'key':
        add_key(args)


def add_key(args: Dict[str, Any]) -> None:
    api_key = ApiKey(args['value'])
    JsonDataManager.save(["api keys", args['name']], api_key)


def add_chatgpt(args: Dict[str, Any]) -> None:
    name = args['name']
    api_key: ApiKey = JsonDataManager.load(["api keys", args['key']], ApiKey)
    sub_model = args.get('sub_model')
    wrapper: GPTWrapper
    if not sub_model:
        wrapper = GPTWrapper(name, api_key.value)
    else:
        wrapper = GPTWrapper(name, api_key.value, sub_model)
    JsonDataManager.save(["models", name], wrapper)

def add_huggingface(args: Dict[str, Any]) -> None:
    name = args['name']
    api_key: ApiKey = JsonDataManager.load(["api keys", args['key']], ApiKey)
    wrapper: HuggingFaceWrapper = HuggingFaceWrapper(name, api_key.value, args['sub_model'])
    JsonDataManager.save(["models", name], wrapper)


def add_dalle(args: Dict[str, Any]) -> None:
    name = args['name']
    api_key: ApiKey = JsonDataManager.load(["api keys", args['key']], ApiKey)
    wrapper: DALLEWrapper = DALLEWrapper(name, api_key=api_key.value, number_of_images=args['num_images'],
                                            resolution=args['res'])
    JsonDataManager.save(["models", name], wrapper)


def add_flow(args: Dict[str, Any]) -> None:
    if args['type'] == 'branching':
            instructions = args['instruction']
            model = ModelLoader.load_model(args['model'])
            b_flow = BranchingFlow(args['name'], model, instructions)
            JsonDataManager.save(["flows", args["name"]], b_flow)
    elif args['type'] == 'seq':
        models = [ModelLoader.load_model(model_name) for model_name in args['multi']]
        flow = SequentialFlow(args['name'], models)
        JsonDataManager.save(["flows", args["name"]], flow)


MODEL_TYPE_TO_CREATION_FUNCTION = {
    'chatgpt': add_chatgpt,
    'dalle': add_dalle,
    'huggingface': add_huggingface,
}