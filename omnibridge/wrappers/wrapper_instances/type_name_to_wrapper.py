from omnibridge.wrappers.wrapper_instances.dalle_wrapper import DALLEWrapper
from omnibridge.wrappers.wrapper_instances.gpt_wrapper import GPTWrapper
from omnibridge.wrappers.wrapper_instances.hugging_face_wrapper import HuggingFaceWrapper


def register_wrapper(cls):
    type_names[cls.get_class_type_field()] = cls
    return cls


type_names = {
    GPTWrapper.get_class_type_field(): GPTWrapper,
    DALLEWrapper.get_class_type_field(): DALLEWrapper,
    HuggingFaceWrapper.get_class_type_field(): HuggingFaceWrapper
}