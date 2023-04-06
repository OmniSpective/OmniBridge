import argparse
from wrappers.runners import run_chatgpt_wrapper, run_dalle_wrapper, run_hugging_face_wrapper
from cli.banner import banner

WRAPPER_TO_FUNC = {
    'chatgpt': run_chatgpt_wrapper,
    'dalle': run_dalle_wrapper,
    'hugging_face': run_hugging_face_wrapper
}


def run() -> int:
    parser = argparse.ArgumentParser(description='AI integration tool.')
    parser.add_argument('-m', '--model', help="name of a model to run", action="append", default=[])
    parser.add_argument('-p', '--prompt', help="prompt for model", action="append", default=[])
    
    args = vars(parser.parse_args())

    models = args["model"]
    prompts = args["prompt"]

    if len(models) != len(prompts):
        print("Can't process args, models length is different than prompts length")
        return 1


    for model, prompt in zip(models, prompts):
        wrapper_func = WRAPPER_TO_FUNC.get(model)

        if not wrapper_func:
            print(f"Skipping {model} model as it is not supported")
            continue

        wrapper_func(prompt)

    return 0


if __name__ == '__main__':
    print(banner)
    exit(run())
