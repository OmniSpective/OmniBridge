from wrappers.chatgpt.gpt_wrapper import GPTConfiguration, GPTWrapper
import argparse
import os


# Temp file for testing requests

parser = argparse.ArgumentParser(description='ChatGPT integration tool.')
parser.add_argument('-p', '--prompt', help="prompt for chatgpt", default="hello")

args = vars(parser.parse_args())

config = GPTConfiguration(model='gpt-3.5-turbo', api_key=os.getenv("OPENAI_API_KEY"))
wrapper = GPTWrapper(prompt=args["prompt"], configuration=config)

print(wrapper())