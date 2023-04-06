from .base_config import BaseConfiguration
from .chatgpt_config import GPTConfiguration
from .dalle_config import DALLEConfiguration
from .hugging_face_config import HuggingFaceConfiguration
from .config_types import ConfigTypes
import os
import json


CONFIG_TYPE_TO_OBJECT = {
    ConfigTypes.CHATGPT: GPTConfiguration,
    ConfigTypes.DALLE: DALLEConfiguration,
    ConfigTypes.HUGGINGFACE: HuggingFaceConfiguration
}


def parse_models_configurations_from_file(config_file_path: str) -> dict[ConfigTypes, BaseConfiguration]:
    """
    Assumes the following JSON structure:
    {
        MODEL_NAME: {
            CONFIG_ATTRIBUTE: CONFIG_VALUE,
            ...
        }
    }

    For example
    {
        chatgpt: {
            api_key: ...,
            model: ...
        },
        dalle: {
            api_key: ...,
            num_of_images: ...,
            resolution: ...
        }
    }
    """
    if not config_file_path or not os.path.exists(config_file_path):
        print(f"Config file not set or doesn't exist, got: {config_file_path}, defaulting to runtime configurations")
        return []

    with open(config_file_path, "r") as f:
        config_json = json.load(f)

    
    models_configs: dict[ConfigTypes, BaseConfiguration] = {}

    for model_name in config_json.keys():
        config_object = CONFIG_TYPE_TO_OBJECT.get(model_name.upper())

        if not config_object:
            print(f"Unsupported model type {model_name}, skipping loading its configuration")
            continue

        try:
            config = config_object(**config_json[model_name])
            models_configs[model_name] = config
        except TypeError:
            print(f"Config of {model_name} is missing required fields, skipping loading its configuration")

    return models_configs
