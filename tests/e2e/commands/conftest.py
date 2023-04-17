import pytest
import json


@pytest.fixture
def saved_data():
    return {
        "models": {
            "gpt3.5": {
                "api key": "mock",
                "model": "gpt-3.5-turbo",
                "_class_type": "chat_gpt"
            },
            "gpt4": {
                "api key": "mock2",
                "model": "gpt-4",
                "_class_type": "chat_gpt"
            }
        },
        "flows": {
            "flow-mock": {
            "_class_type": "branching",
            "root_model": "gpt3.5",
            "branched_models": "gpt3.5, gpt3.5, gpt3.5",
            "instructions": "expand point 1$$$expand point 2$$$expand point 3"
            }
        },
        "api keys": {
            "key-mock": {
                "value": "mock"
            }
        }
    }


@pytest.fixture
def saved_data_fixture(saved_data):
    def _saved_data_for_tests(file_path):
        with open(file_path, 'w') as f:
            f.write(json.dumps(saved_data, indent=2))

    return _saved_data_for_tests