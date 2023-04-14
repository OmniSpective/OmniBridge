import json
import os
from abc import ABC, abstractmethod
from typing import Dict, Type

FILE_NAME = ".saved_data.json"
MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(MODULE_DIR, FILE_NAME)


class JsonConvertable(ABC):
    @abstractmethod
    def to_json(self) -> Dict[str, str]:
        pass

    @classmethod
    @abstractmethod
    def create_from_json(cls, json_data: Dict[str, str]):
        pass


class JsonDataManager:
    @staticmethod
    def save(nested_key: str, item: JsonConvertable) -> None:
        json_value = item.to_json()
        keys = nested_key.split('.')

        data = {}
        if os.path.isfile(FILE_PATH):
            with open(FILE_PATH, 'r') as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    pass

        current_data = data
        for key in keys[:-1]:
            current_data = current_data.setdefault(key, {})

        current_data[keys[-1]] = json_value

        with open(FILE_PATH, 'w') as f:
            json.dump(data, f, indent=2)

    @staticmethod
    def load(nested_key: str, cls: Type[JsonConvertable]):
        if not os.path.exists(FILE_PATH):
            raise FileNotFoundError("Saved data file cannot be found.")

        with open(FILE_PATH, "r") as f:
            data = json.load(f)
            keys = nested_key.split('.')
            for key in keys:
                try:
                    data = data[key]
                except KeyError:
                    raise KeyError(f"Key '{key}' not found in JSON data")
            return cls.create_from_json(data)
