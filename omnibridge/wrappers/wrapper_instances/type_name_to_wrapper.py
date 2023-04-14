from omnibridge.wrappers.wrapper_instances.base_api_wrapper import RestAPIWrapper
from omnibridge.wrappers.wrapper_instances.dalle_wrapper import DALLEWrapper
from omnibridge.wrappers.wrapper_instances.gpt_wrapper import GPTWrapper

type_names = {
    GPTWrapper.get_class_type_field(): GPTWrapper,
    DALLEWrapper.get_class_type_field(): DALLEWrapper
}
