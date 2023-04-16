import json
import os
from abc import ABC, abstractmethod
from typing import Dict, Type, List, Union, Any

FILE_NAME = ".saved_data.json"
MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(MODULE_DIR, FILE_NAME)


class JsonConvertable(ABC):
    @abstractmethod
    def to_json(self) -> Dict[str, Union[str, int]]:
        pass

    @classmethod
    @abstractmethod
    def create_from_json(cls, json_key: str, json_data: Dict[str, str]) -> Any:
        pass


class JsonDataManager:
    @staticmethod
    def save(nested_path: List[str], item: JsonConvertable) -> None:
        json_value = item.to_json()

        data = {}
        if os.path.isfile(FILE_PATH):
            with open(FILE_PATH, 'r') as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    pass

        current_data = data
        for key in nested_path[:-1]:
            current_data = current_data.setdefault(key, {})

        current_data[nested_path[-1]] = json_value

        with open(FILE_PATH, 'w') as f:
            json.dump(data, f, indent=2)

    @staticmethod
    def load(nested_path: List[str], cls: Type[JsonConvertable]) -> Any:
        data = JsonDataManager.get_json_value(nested_path)
        if len(nested_path) == 0:
            json_key = ""
        else:
            json_key = nested_path[-1]
        return cls.create_from_json(json_key, data)

    @staticmethod
    def get_json_value(nested_path: List[str]) -> Any:
        if not os.path.exists(FILE_PATH):
            raise FileNotFoundError("Saved data file cannot be found.")

        with open(FILE_PATH, "r") as f:
            data = json.load(f)
            for key in nested_path:
                try:
                    data = data[key]
                except KeyError:
                    raise KeyError(f"Key '{key}' not found in JSON data")
            return data
