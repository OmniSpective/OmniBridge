from wrappers.api_based_wrappers.gpt_wrapper import GPTConfiguration, GPTWrapper
import os

# ---------------- CHATGPT ----------------------------
config = GPTConfiguration(model='gpt-3.5-turbo', api_key="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")
wrapper = GPTWrapper(prompt="hello", configuration=config)

print(wrapper())

# ---------------- DALLE ----------------------------
from wrappers.api_based_wrappers.dalle_wrapper import DALLEWrapper, DALLEConfiguration

config = DALLEConfiguration(api_key="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",
                            resolution='256x256',
                            images=4)
wrapper = DALLEWrapper(prompt="dog", configuration=config)
wrapper()

# ---------------- HUGGINGFACE ----------------------------
from wrappers.api_based_wrappers.hugging_face_wrapper import HuggingFaceConfiguration, HuggingFaceWrapper

config = HuggingFaceConfiguration(api_key="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",
                            model_id = "distilbert-base-uncased")
                            
wrapper = HuggingFaceWrapper(prompt="The goal of life is [MASK].", configuration=config)
wrapper()