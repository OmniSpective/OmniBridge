import argparse

from omnibridge.model_entities.models_io.base_model_io import TextualIO
from omnibridge.saved_data.json_data_manager import JsonDataManager
from omnibridge.wrappers.api_key import ApiKey
from omnibridge.cli.banner import banner
from omnibridge.wrappers.wrapper_instances.dalle_wrapper import DALLEWrapper
from omnibridge.wrappers.wrapper_instances.gpt_wrapper import GPTWrapper
from omnibridge.wrappers.wrapper_instances.type_name_to_wrapper import type_names


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

    args = vars(parser.parse_args())
    if args['command'] == 'add-key':
        api_key = ApiKey(args['value'])
        JsonDataManager.save(["api keys", args['name']], api_key)
        return 0
    elif args['command'] == 'add-chatgpt':
        api_key: ApiKey = JsonDataManager.load(["api keys", args['key']], ApiKey)
        wrapper: GPTWrapper = GPTWrapper(api_key.value, args['model'])
        JsonDataManager.save(["models", args['name']], wrapper)
        return 0
    elif args['command'] == 'add-dalle':
        api_key: ApiKey = JsonDataManager.load(["api keys", args['key']], ApiKey)
        wrapper: DALLEWrapper = DALLEWrapper(api_key=api_key.value, number_of_images=args['num_images'],
                                             resolution=args['res'])
        JsonDataManager.save(["models", args['name']], wrapper)
        return 0
    elif args['prompt'] and args['model_name']:
        class_type_name = JsonDataManager.get_json_value(["models", args['model_name'], "_class_type"])
        wrapper_type = type_names[class_type_name]
        wrapper = JsonDataManager.load(["models", args['model_name']], wrapper_type)
        response = wrapper.process(TextualIO(args['prompt']))
        print(response)
        return 0

    return 1


def main():
    print(banner)
    exit(run())


if __name__ == '__main__':
    main()
