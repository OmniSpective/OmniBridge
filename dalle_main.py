import os
import argparse
from wrappers.api_based_wrappers.dalle_wrapper import DALLEWrapper, DALLEConfiguration


parser = argparse.ArgumentParser(description='DALL-E integration tool.')
parser.add_argument('-p', '--prompt', help="prompt for DALL-E", default="dog")

args = vars(parser.parse_args())

config = DALLEConfiguration(api_key=os.getenv("OPENAI_API_KEY"),
                            resolution='256x256',
                            images=4)
wrapper = DALLEWrapper(prompt=args["prompt"], configuration=config)
wrapper()
