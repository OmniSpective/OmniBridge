import subprocess
from omnibridge.saved_data.json_data_manager import JsonDataManager


def test_create_key():
    # Arrange
    command = ["pipenv", "run", "python", "./main.py", "create", "key", "-n", "test_key", "-v", "mock"]

    # Act
    subprocess.run(command)
    result = JsonDataManager.get_json_value(["api keys", "test_key"])

    # Assert
    assert result == {'value': 'mock'}


def test_create_model(create_key_fixture):
    # Arrange
    model_name = "test_model"
    command = ["pipenv", "run", "python", "./main.py", "create", "model", "chatgpt", "-n", model_name, "-k", "test_key"]

    # Act
    subprocess.run(command)
    result = JsonDataManager.get_json_value(["models", model_name])

    # Assert
    assert result == {
        "api key": "mock",
        "model": "gpt-3.5-turbo",
        "_class_type": "chat_gpt"
    }


def test_create_model_with_sub_model(create_key_fixture):
    # Arrange
    model_name = "test_model"
    command = ["pipenv", "run", "python", "./main.py", "create", "model",
                "chatgpt", "-n", model_name, "-k", "test_key", "--sub-model", "gpt-4"]

    # Act
    subprocess.run(command)
    result = JsonDataManager.get_json_value(["models", model_name])

    # Assert
    assert result == {
        "api key": "mock",
        "model": "gpt-4",
        "_class_type": "chat_gpt"
    }


def test_create_flow(create_model_fixture):
    # Arrange
    flow_name = "test_flow"
    model_name = "test_model"
    prompt1 = "prompt1"
    prompt2 = "prompt2"
    command = ["pipenv", "run", "python", "./main.py", "create", "flow",
                "--name", flow_name, "--model", model_name, "-i", prompt1, prompt2]

    # Act
    subprocess.run(command)
    result = JsonDataManager.get_json_value(["flows", flow_name])

    # Assert
    assert result == {
        '_class_type': 'branching',
        'root_model': model_name,
        'branched_models': f'{model_name}, {model_name}',
        'instructions': f'{prompt1}$$${prompt2}'
    }