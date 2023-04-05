import os
from wrappers.api_based_wrappers.dalle_wrapper import DALLEWrapper, DALLEConfiguration

config = DALLEConfiguration(api_key=os.getenv("OPENAI_API_KEY"),
                            resolution='256x256',
                            images=4)
wrapper = DALLEWrapper(prompt="dog", configuration=config)
wrapper()
