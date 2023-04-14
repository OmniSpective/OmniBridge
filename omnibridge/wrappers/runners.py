from omnibridge.wrappers.wrapper_instances.gpt_wrapper import GPTWrapper
from omnibridge.wrappers.wrapper_instances.dalle_wrapper import DALLEWrapper
from omnibridge.wrappers.wrapper_instances.hugging_face_wrapper import HuggingFaceWrapper
from omnibridge.wrappers.wrapper_instance_configurations.base_config import BaseConfiguration
from omnibridge.wrappers.wrapper_instance_configurations.chatgpt_config import GPTConfiguration
from omnibridge.wrappers.wrapper_instance_configurations.dalle_config import DALLEConfiguration
from omnibridge.wrappers.wrapper_instance_configurations.hugging_face_config import HuggingFaceConfiguration
from omnibridge.common.logging.log_manager import LogManager
import os
from typing import Any, cast, Optional

logger = LogManager().logger

def run_prompt_in_chatgpt_wrapper(prompt: str, config: Optional[BaseConfiguration] = None) -> Any:
    if config:
        config = cast(GPTConfiguration, config)
    else:
        config = GPTConfiguration(model='gpt-3.5-turbo', 
                                  api_key=os.getenv("OPENAI_API_KEY", ""))
        
    wrapper = GPTWrapper(configuration=config)

    try:
        response = wrapper.prompt_and_get_response(prompt)
        print(response)
        return response
    except Exception as e:
        print(e)

    return None


def run_prompt_in_dalle_wrapper(prompt: str, config: Optional[BaseConfiguration] = None) -> Any:
    if config:
        config = cast(DALLEConfiguration, config)
    else:
        config = DALLEConfiguration(api_key=os.getenv("OPENAI_API_KEY", ""),
                                                       resolution='256x256',
                                                       num_of_images=4)
        
    wrapper = DALLEWrapper(configuration=config, logger=logger)

    try:
        ret = wrapper.prompt_and_generate_files(prompt)
        return ret
    except Exception as e:
        print(e)

    return None


def run_prompt_in_hugging_face_wrapper(prompt: str, config: Optional[BaseConfiguration] = None) -> Any:
    if config:
        config = cast(HuggingFaceConfiguration, config)
    else:
        config = HuggingFaceConfiguration(api_key=os.getenv("HUGGING_FACE_API_KEY", ""), 
                                          model_id="distilbert-base-uncased")

    wrapper = HuggingFaceWrapper(configuration=config, logger=logger)

    try:
        ret = wrapper.prompt(prompt)
        return ret
    except Exception as e:
        print(e)

    return None
