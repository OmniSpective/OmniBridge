from wrappers.api_based_wrappers.gpt_wrapper import GPTConfiguration, GPTWrapper
from wrappers.api_based_wrappers.dalle_wrapper import DALLEWrapper, DALLEConfiguration
from wrappers.api_based_wrappers.hugging_face_wrapper import HuggingFaceConfiguration, HuggingFaceWrapper
import os

def run_chatgpt_wrapper(prompt: str):
    config = GPTConfiguration(model='gpt-3.5-turbo', api_key=os.getenv("OPENAI_API_KEY"))
    wrapper = GPTWrapper(prompt=prompt, configuration=config)

    try:
        print(wrapper())
    except Exception as e:
        print(e)

def run_dalle_wrapper(prompt: str):
    config = DALLEConfiguration(api_key=os.getenv("OPENAI_API_KEY"),
                                resolution='256x256',
                                num_of_images=4)
    wrapper = DALLEWrapper(prompt=prompt, configuration=config)

    try:
        wrapper()
    except Exception as e:
        print(e)

def run_hugging_face_wrapper(prompt: str):
    config = HuggingFaceConfiguration(api_key=os.getenv("HUGGING_FACE_API_KEY"),
                            model_id = "distilbert-base-uncased")        
    wrapper = HuggingFaceWrapper(prompt=prompt, configuration=config)
    
    try:
        wrapper()
    except Exception as e:
        print(e)
