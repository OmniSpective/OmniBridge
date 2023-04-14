from omnibridge.model_entities.models_io.base_model_io import TextualIO
from omnibridge.saved_data.json_data_manager import JsonDataManager
from omnibridge.wrappers.api_key import ApiKey
from omnibridge.wrappers.wrapper_instances.gpt_wrapper import GPTWrapper
from omnibridge.wrappers.wrapper_instances.dalle_wrapper import DALLEWrapper
from omnibridge.wrappers.wrapper_instances.hugging_face_wrapper import HuggingFaceWrapper
from omnibridge.common.logging.log_manager import LogManager
from typing import Any

logger = LogManager().logger


def run_prompt_in_chatgpt_wrapper(prompt: str, model: str = 'gpt-3.5-turbo', api_key: str = "") -> Any:
    wrapper = GPTWrapper(model=model, api_key=api_key)

    try:
        response = wrapper.process(TextualIO(prompt))
        print(response)
        return response
    except Exception as e:
        print(e)

    return None


def run_prompt_in_dalle_wrapper(prompt: str) -> Any:
    api_key = JsonDataManager.load(["api keys", "open api"], ApiKey)

    wrapper = DALLEWrapper(api_key=api_key, resolution="256x256", number_of_images=4, logger=logger)

    try:
        ret = wrapper.process(TextualIO(prompt))
        return ret
    except Exception as e:
        print(e)

    return None


def run_prompt_in_hugging_face_wrapper(prompt: str) -> Any:
    api_key = JsonDataManager.load(["api keys", "hugging_face"], ApiKey)
    model_id = "distilbert-base-uncased"

    wrapper = HuggingFaceWrapper(api_key=api_key, model=model_id, logger=logger)

    try:
        ret = wrapper.process(TextualIO(prompt))
        return ret
    except Exception as e:
        print(e)

    return None
