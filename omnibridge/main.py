import argparse
from omnibridge.wrappers.runners import run_prompt_in_chatgpt_wrapper, run_prompt_in_dalle_wrapper, \
    run_prompt_in_hugging_face_wrapper
from omnibridge.wrappers.wrapper_instance_configurations.config_loader import parse_models_configurations_from_file
from omnibridge.wrappers.wrapper_instance_configurations.config_types import ConfigTypes
from omnibridge.cli.banner import banner
from typing import Callable, Any, Optional, Dict
from omnibridge.wrappers.wrapper_instance_configurations.base_config import BaseConfiguration


WRAPPER_TO_FUNC: Dict[str, Callable[[str, Optional[BaseConfiguration]], Any]] = {
    'chatgpt': run_prompt_in_chatgpt_wrapper,
    'dalle': run_prompt_in_dalle_wrapper,
    'hugging_face': run_prompt_in_hugging_face_wrapper
}


def run() -> int:
    parser = argparse.ArgumentParser(description='AI integration tool.')
    parser.add_argument('-m', '--model', help="name of a model to run", action="append", default=[])
    parser.add_argument('-p', '--prompt', help="prompt for model", action="append", default=[])
    parser.add_argument('-l', "--load-config", help="absolute path to models configuration file")

    args = vars(parser.parse_args())

    models = args["model"]
    prompts = args["prompt"]

    if len(models) != len(prompts):
        print("Can't process args, models length is different than prompts length")
        return 1

    configs = parse_models_configurations_from_file(args["load_config"])

    for model, prompt in zip(models, prompts):
        wrapper_func = WRAPPER_TO_FUNC.get(model)

        if not wrapper_func:
            print(f"Skipping {model} model as it is not supported")
            continue
        
        config = configs.get(ConfigTypes(model.upper())) if configs else None
        wrapper_func(prompt, config)

    return 0


def main():
    print(banner)
    exit(run())


if __name__ == '__main__':
    main()
