from abc import abstractmethod

from omnibridge.saved_data.json_data_manager import JsonConvertable
from omnibridge.wrappers.wrapper_interfaces.processor import Processor


class ModelWrapper(JsonConvertable, Processor):
    @abstractmethod
    def get_name(self) -> str:
        pass

    @classmethod
    @abstractmethod
    def get_class_type_field(cls) -> str:
        pass
