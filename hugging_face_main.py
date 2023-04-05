import os
from wrappers.api_based_wrappers.hugging_face_wrapper import HuggingFaceConfiguration, HuggingFaceWrapper

config = HuggingFaceConfiguration(api_key=os.getenv("HUGGING_FACE_API_TOKEN"),
                            model_id = "distilbert-base-uncased")
                            
wrapper = HuggingFaceWrapper(prompt="The goal of life is [MASK].", configuration=config)
wrapper()
