from typing import Dict, Union, Any

from omnibridge.saved_data.json_data_manager import JsonConvertable


class ApiKey(JsonConvertable):
    def __init__(self, value: str):
        self.value = value

    def to_json(self) -> Dict[str, Union[str, int]]:
        return {
            'value': self.value
        }

    @classmethod
    def create_from_json(cls, json_key: str, json_data: Dict[str, str]) -> Any:
        return ApiKey(json_data['value'])
