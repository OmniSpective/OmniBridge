from typing import Dict, Any
from omnibridge.wrappers.wrapper_instances.type_name_to_wrapper import type_names
from omnibridge.saved_data.json_data_manager import JsonDataManager
import json


def handle_list_command(args: Dict[str, Any]) -> None:
    func = OBJECT_TO_LIST_FUNCTION.get(args['object_to_list'])

    if not func:
        return
    
    func()


def list_wrappers() -> None:
    print([type for type in type_names.keys()])


def list_keys() -> None:
    try:
        keys = JsonDataManager.get_json_value(['api keys'])
        print(json.dumps(keys, indent=2))
    except KeyError:
        print('No keys were found in your saved data')
    

def list_models() -> None:
    try:
        models = JsonDataManager.get_json_value(['models'])
        print(json.dumps(models, indent=2))
    except KeyError:
        print('No models were found in your saved data')



def list_flows() -> None:
    try:
        flows = JsonDataManager.get_json_value(['flows'])
        print(json.dumps(flows, indent=2))
    except KeyError:
        print('No flows were found in your saved data')
   


OBJECT_TO_LIST_FUNCTION = {
    'wrappers': list_wrappers,
    'keys': list_keys,
    'models': list_models,
    'flows': list_flows
}