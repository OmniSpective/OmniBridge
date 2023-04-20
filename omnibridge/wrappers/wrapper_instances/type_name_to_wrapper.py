from typing import Dict, Type

from omnibridge.saved_data.json_data_manager import JsonDataManager, JsonConvertable
from omnibridge.wrappers.wrapper_instances.dalle_wrapper import DALLEWrapper
from omnibridge.wrappers.wrapper_instances.gpt_wrapper import GPTWrapper
from omnibridge.wrappers.wrapper_instances.hugging_face_wrappers import HuggingFaceWrapper
from omnibridge.wrappers.wrapper_interfaces.model_wrapper import ModelWrapper

type_names: Dict[str, Type[JsonConvertable]] = {
    GPTWrapper.get_class_type_field(): GPTWrapper,
    DALLEWrapper.get_class_type_field(): DALLEWrapper,
    HuggingFaceWrapper.get_class_type_field(): HuggingFaceWrapper
}


class ModelLoader:
    @staticmethod
    def load_model(model_name: str) -> ModelWrapper:
        class_type_name = JsonDataManager.get_json_value(["models", model_name, "_class_type"])
        wrapper_type = type_names[class_type_name]
        wrapper: ModelWrapper = JsonDataManager.load(["models", model_name], wrapper_type)
        return wrapper
