import subprocess
from omnibridge.wrappers.wrapper_instances.type_name_to_wrapper import type_names
from omnibridge.cli.banner import banner
from omnibridge.saved_data.json_data_manager import FILE_PATH
import json


def test_list_wrappers():
    # Arrange
    command = ["pipenv", "run", "python", "./main.py", "list", "wrappers"]

    # Act
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    result_without_banner = result.stdout.strip(banner)

    # Assert
    assert result_without_banner == f'{[type for type in type_names.keys()]}'


def test_list_keys(saved_data_fixture):
    # Arrange
    command = ["pipenv", "run", "python", "./main.py", "list", "keys"]
    saved_data_fixture(FILE_PATH)

    # Act
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    result_without_banner = result.stdout.strip(banner)

    # Assert
    assert result_without_banner == json.dumps(
        {
            "key-mock": {
                "value": "mock"
            }
        },
        indent=2
    )

def test_list_keys_empty(saved_data_fixture):
    # Arrange
    command = ["pipenv", "run", "python", "./main.py", "list", "keys"]
    saved_data_fixture(FILE_PATH, no_keys=True)

    # Act
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    result_without_banner = result.stdout.strip(banner)

    # Assert
    assert result_without_banner == 'No keys were found in your saved data'


def test_list_models(saved_data_fixture):
    # Arrange
    command = ["pipenv", "run", "python", "./main.py", "list", "models"]
    saved_data_fixture(FILE_PATH)

    # Act
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    result_without_banner = result.stdout.strip(banner)

    # Assert
    assert result_without_banner == json.dumps(
        {
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
        indent=2
    )

def test_list_models_empty(saved_data_fixture):
    # Arrange
    command = ["pipenv", "run", "python", "./main.py", "list", "models"]
    saved_data_fixture(FILE_PATH, no_models=True)

    # Act
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    result_without_banner = result.stdout.strip(banner)

    # Assert
    assert result_without_banner == 'No models were found in your saved data'


def test_list_flows(saved_data_fixture):
    # Arrange
    command = ["pipenv", "run", "python", "./main.py", "list", "flows"]
    saved_data_fixture(FILE_PATH)

    # Act
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    result_without_banner = result.stdout.strip(banner)

    # Assert
    assert result_without_banner == json.dumps(
        {
            "flow-mock": {
                "_class_type": "branching",
                "root_model": "gpt3.5",
                "branched_models": "gpt3.5, gpt3.5, gpt3.5",
                "instructions": "expand point 1$$$expand point 2$$$expand point 3"
            }
        },
        indent=2
    )

def test_list_flows_empty(saved_data_fixture):
    # Arrange
    command = ["pipenv", "run", "python", "./main.py", "list", "flows"]
    saved_data_fixture(FILE_PATH, no_flows=True)

    # Act
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    result_without_banner = result.stdout.strip(banner)

    # Assert
    assert result_without_banner == 'No flows were found in your saved data'