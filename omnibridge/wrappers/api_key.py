from typing import Dict

from omnibridge.saved_data.json_data_manager import JsonConvertable


class ApiKey(JsonConvertable):
    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value

    def to_json(self) -> Dict[str, str]:
        return {
            'name': self.name,
            'value': self.value
        }

    @classmethod
    def create_from_json(cls, json_data: Dict[str, str]):
        return ApiKey(json_data['name'], json_data['value'])
