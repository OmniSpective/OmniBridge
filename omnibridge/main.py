import argparse

from omnibridge.flows.branching_flow import BranchingFlow
from omnibridge.flows.flow_loader import FlowLoader
from omnibridge.flows.sequential_flow import SequentialFlow
from omnibridge.model_entities.models_io.base_model_io import TextualIO
from omnibridge.saved_data.json_data_manager import JsonDataManager
from omnibridge.wrappers.api_key import ApiKey
from omnibridge.cli.banner import banner
from omnibridge.wrappers.wrapper_instances.dalle_wrapper import DALLEWrapper
from omnibridge.wrappers.wrapper_instances.gpt_wrapper import GPTWrapper
from omnibridge.wrappers.wrapper_instances.type_name_to_wrapper import ModelLoader


def run() -> int:
    parser = argparse.ArgumentParser(description='AI integration tool.')
    parser.add_argument('-p', '--prompt', help="prompt for model", type=str, default=[])
    parser.add_argument('-l', "--load-config", help="absolute path to models configuration file")
    parser.add_argument('-n', "--model-name", help="which model to use.")

    subparsers = parser.add_subparsers(help='sub-command help', dest='command')
    api_key_parser = subparsers.add_parser("add-key", help="Add an api key.")
    api_key_parser.add_argument('-n', '--name', help="name of the api key.", type=str, required=True)
    api_key_parser.add_argument('-v', '--value', help="value of the api key.", type=str, required=True)

    add_chatgpt_model_parser = subparsers.add_parser("add-chatgpt", help="add chatgpt model connection details.")
    add_chatgpt_model_parser.add_argument('-n', '--name', type=str, required=True,
                                          help="name of the model, e.g. my_gpt4.")
    add_chatgpt_model_parser.add_argument('-k', '--key', type=str, required=True, help="api key name.")
    add_chatgpt_model_parser.add_argument('-m', '--model', type=str, default="gpt-3.5-turbo",
                                          help="model, e.g. 3.5 or 4.")

    add_chatgpt_model_parser = subparsers.add_parser("add-dalle", help="add dalle model.")
    add_chatgpt_model_parser.add_argument('-n', '--name', type=str, required=True, help="name of the model.")
    add_chatgpt_model_parser.add_argument('-k', '--key', type=str, required=True, help="api key name.")
    add_chatgpt_model_parser.add_argument('--num-images', type=str, default="4",
                                          help="number of images per prompt, default 4.")
    add_chatgpt_model_parser.add_argument('-r', '--res', type=str, default="256x256", help="resolution of images.")

    add_chatgpt_model_parser = subparsers.add_parser("add-flow", help="add flow.")
    add_chatgpt_model_parser.add_argument('-n', '--name', type=str, required=True, help="name of the flow.")
    add_chatgpt_model_parser.add_argument('-t', '--type', type=str, choices=['seq', 'branching'], default='branching',
                                          help="type of the flow.")
    add_chatgpt_model_parser.add_argument('-m', '--model', type=str,
                                          help="name of the model to use.")
    add_chatgpt_model_parser.add_argument('-i', '--instruction', nargs='*', type=str,
                                          help="instruct the model to do something with the input.")
    add_chatgpt_model_parser.add_argument('--multi', nargs='*', type=str,
                                          help="use multiple models. Currently only supported in sequential flow.")

    add_chatgpt_model_parser = subparsers.add_parser("run-flow", help="run flow.")
    add_chatgpt_model_parser.add_argument('-n', '--name', type=str, required=True, help="name of the flow.")
    add_chatgpt_model_parser.add_argument('-p', '--prompt', help="prompt for flow", type=str, required=True)

    args = vars(parser.parse_args())
    if args['command'] == 'run-flow':
        flow = FlowLoader.load_flow(args['name'])
        flow_input = TextualIO(args['prompt'])
        flow_output = flow.process(flow_input)
        print(flow_output)
        return 0
    if args['command'] == 'add-flow':
        if args['type'] == 'branching':
            instructions = args['instruction']
            model = ModelLoader.load_model(args['model'])
            b_flow = BranchingFlow(args['name'], model, instructions)
            JsonDataManager.save(["flows", args["name"]], b_flow)
            return 0
        if args['type'] == 'seq':
            models = [ModelLoader.load_model(model_name) for model_name in args['multi']]
            flow = SequentialFlow(args['name'], models)
            JsonDataManager.save(["flows", args["name"]], flow)
            return 0
    if args['command'] == 'add-key':
        api_key = ApiKey(args['value'])
        JsonDataManager.save(["api keys", args['name']], api_key)
        return 0
    elif args['command'] == 'add-chatgpt':
        api_key: ApiKey = JsonDataManager.load(["api keys", args['key']], ApiKey)
        wrapper: GPTWrapper = GPTWrapper(args['name'], api_key.value, args['model'])
        JsonDataManager.save(["models", args['name']], wrapper)
        return 0
    elif args['command'] == 'add-dalle':
        api_key: ApiKey = JsonDataManager.load(["api keys", args['key']], ApiKey)
        wrapper: DALLEWrapper = DALLEWrapper(name=args['name'], api_key=api_key.value,
                                             number_of_images=args['num_images'], resolution=args['res'])
        JsonDataManager.save(["models", args['name']], wrapper)
        return 0
    elif args['prompt'] and args['model_name']:
        wrapper = ModelLoader.load_model(model_name=args['model_name'])
        response = wrapper.process(TextualIO(args['prompt']))
        print(response)
        return 0

    return 1


def main():
    print(banner)
    exit(run())


if __name__ == '__main__':
    main()
