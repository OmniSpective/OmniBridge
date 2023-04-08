from .api_based_wrappers.gpt_wrapper import GPTConfiguration, GPTWrapper
from .api_based_wrappers.dalle_wrapper import DALLEWrapper, DALLEConfiguration
from .api_based_wrappers.hugging_face_wrapper import HuggingFaceConfiguration, HuggingFaceWrapper
import os
from typing import Dict, Any


def run_chatgpt_wrapper(prompt: str, config: GPTConfiguration | None = None) -> Dict[str, Any]:
    _config = config if config else GPTConfiguration(model='gpt-3.5-turbo',
                                                      api_key=os.getenv("OPENAI_API_KEY"))
    wrapper = GPTWrapper(prompt=prompt, configuration=_config)

    try:
        ret = print(wrapper())
        return ret
    except Exception as e:
        print(e)

    

def run_dalle_wrapper(prompt: str, config: DALLEConfiguration | None = None) -> Dict[str, Any]:
    _config = config if config else DALLEConfiguration(api_key=os.getenv("OPENAI_API_KEY"),
                                                        resolution='256x256',
                                                        num_of_images=4)
    wrapper = DALLEWrapper(prompt=prompt, configuration=_config)

    try:
        ret = wrapper()
        return ret
    except Exception as e:
        print(e)

    

def run_hugging_face_wrapper(prompt: str, config: HuggingFaceConfiguration) -> Dict[str, Any]:
    _config = config if config else HuggingFaceConfiguration(
        api_key=os.getenv("HUGGING_FACE_API_KEY"),
        model_id = "distilbert-base-uncased")        
    wrapper = HuggingFaceWrapper(prompt=prompt, configuration=_config)
    
    try:
        ret = wrapper()
        return ret
    except Exception as e:
        print(e)

    