from wrappers.api_based_wrappers.gpt_wrapper import GPTConfiguration, GPTWrapper
import argparse
import os

# ---------------- CHATGPT ----------------------------
parser = argparse.ArgumentParser(description='ChatGPT integration tool.')
parser.add_argument('-p', '--prompt', help="prompt for chatgpt", default="hello")

args = vars(parser.parse_args())

config = GPTConfiguration(model='gpt-3.5-turbo', api_key="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")
wrapper = GPTWrapper(prompt=args["prompt"], configuration=config)

print(wrapper())

# ---------------- DALLE ----------------------------
from wrappers.api_based_wrappers.dalle_wrapper import DALLEWrapper, DALLEConfiguration

parser = argparse.ArgumentParser(description='DALL-E integration tool.')
parser.add_argument('-p', '--prompt', help="prompt for DALL-E", default="dog")

args = vars(parser.parse_args())

config = DALLEConfiguration(api_key="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",
                            resolution='256x256',
                            images=4)
wrapper = DALLEWrapper(prompt=args["prompt"], configuration=config)
wrapper()

# ---------------- HUGGINGFACE ----------------------------
from wrappers.api_based_wrappers.hugging_face_wrapper import HuggingFaceConfiguration, HuggingFaceWrapper

config = HuggingFaceConfiguration(api_key="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",
                            model_id = "distilbert-base-uncased")
                            
wrapper = HuggingFaceWrapper(prompt="The goal of life is [MASK].", configuration=config)
wrapper()