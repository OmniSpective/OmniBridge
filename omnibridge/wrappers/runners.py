from .api_based_wrappers.gpt_wrapper import GPTConfiguration, GPTWrapper
from .api_based_wrappers.dalle_wrapper import DALLEWrapper, DALLEConfiguration
from .api_based_wrappers.hugging_face_wrapper import HuggingFaceConfiguration, HuggingFaceWrapper
from omnibridge.common.logging.log_manager import LogManager
import os
from typing import Dict, Any

logger = LogManager().logger


def run_prompt_in_chatgpt_wrapper(prompt: str, config: GPTConfiguration | None = None) -> Any:
    _config = config if config else GPTConfiguration(model='gpt-3.5-turbo',
                                                     api_key=os.getenv("OPENAI_API_KEY"))
    wrapper = GPTWrapper(configuration=_config, logger=logger)

    try:
        response = wrapper.prompt_and_get_response(prompt)
        print(response)
        return response
    except Exception as e:
        print(e)


def run_prompt_in_dalle_wrapper(prompt: str, config: DALLEConfiguration | None = None) -> Any:
    _config = config if config else DALLEConfiguration(api_key=os.getenv("OPENAI_API_KEY"),
                                                       resolution='256x256',
                                                       num_of_images=4)
    wrapper = DALLEWrapper(configuration=_config, logger=logger)

    try:
        ret = wrapper.prompt_and_generate_files(prompt)
        return ret
    except Exception as e:
        print(e)


def run_prompt_in_hugging_face_wrapper(prompt: str, config: HuggingFaceConfiguration) -> Dict[str, Any]:
    _config = config if config else HuggingFaceConfiguration(
        api_key=os.getenv("HUGGING_FACE_API_KEY"),
        model_id="distilbert-base-uncased")
    wrapper = HuggingFaceWrapper(configuration=_config, logger=logger)

    try:
        ret = wrapper.prompt(prompt)
        return ret
    except Exception as e:
        print(e)
