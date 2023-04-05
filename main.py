from wrappers.chatgpt.gpt_wrapper import GPTConfiguration, GPTWrapper
import os


# Temp file for testing requests


config = GPTConfiguration(model='gpt-3.5-turbo', api_key=os.getenv("OPENAI_API_KEY"))
wrapper = GPTWrapper(prompt="hello", configuration=config)

wrapper()