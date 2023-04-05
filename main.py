from wrappers.api_based_wrappers.gpt_wrapper import GPTConfiguration, GPTWrapper
from wrappers.api_based_wrappers.dalle_wrapper import DALLEWrapper, DALLEConfiguration
from wrappers.api_based_wrappers.hugging_face_wrapper import HuggingFaceConfiguration, HuggingFaceWrapper

import argparse
import os
import sys

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
    config = HuggingFaceConfiguration(api_key=os.getenv("OPENAI_API_KEY"),
                            model_id = "distilbert-base-uncased")        
    wrapper = HuggingFaceWrapper(prompt=prompt, configuration=config)
    
    try:
        wrapper()
    except Exception as e:
        print(e)


WRAPPER_TO_FUNC = {
    'chatgpt': run_chatgpt_wrapper,
    'dalle': run_dalle_wrapper,
    'hugging_face': run_hugging_face_wrapper
}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='ntegration tool.')
    parser.add_argument('-dp', '--dalle_prompt', help="prompt for DALL-E", default="dog")
    parser.add_argument('-cp', '--chatgpt_prompt', help="prompt for chatgpt", default="hello")
    parser.add_argument('-hp', '--hugging_face_prompt', help='prompt for hugging face',
                         default="The goal of life is [MASK].")
    parser.add_argument('-r', '--run_wrapper', help='wrappers to run', action='append', 
                        default=[])
    
    args = vars(parser.parse_args())
    print(args)
    wrappers_names_to_run = args["run_wrapper"]
    print(wrappers_names_to_run)

    if not wrappers_names_to_run:
        run_chatgpt_wrapper(args["chatgpt_prompt"])
        run_dalle_wrapper(args["dalle_prompt"])
        run_hugging_face_wrapper(args["hugging_face_prompt"])
        exit(0)

    for wrapper_name in wrappers_names_to_run:
        WRAPPER_TO_FUNC[wrapper_name](args[f'{wrapper_name}_prompt'])

    
    

