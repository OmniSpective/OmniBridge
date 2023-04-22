import subprocess

from omnibridge.flows.branching_flow import BranchingFlow
from omnibridge.saved_data.json_data_manager import JsonDataManager
from omnibridge.wrappers.api_key import ApiKey
from omnibridge.wrappers.wrapper_instances.gpt_wrapper import GPTWrapper


def test_create_key(cwd):
    # Arrange
    command = ["pipenv", "run", "python", "./main.py", "create", "key", "-n", "test_key", "-v", "mock"]

    # Act
    subprocess.run(command, cwd=cwd)
    key = JsonDataManager.load(["api keys", "test_key"], ApiKey)

    # Assert
    assert key.value == 'mock'


def test_create_model(create_key_fixture, cwd):
    # Arrange
    model_name = "test_model"
    command = ["pipenv", "run", "python", "./main.py", "create", "model", "chatgpt", "-n", model_name, "-k", "test_key"]

    # Act
    subprocess.run(command, cwd=cwd)
    model = JsonDataManager.load(["models", model_name], GPTWrapper)

    # Assert
    assert model.api_key == 'mock'
    assert model.model == 'gpt-3.5-turbo'


def test_create_model_with_sub_model(create_key_fixture, cwd):
    # Arrange
    model_name = "test_model"
    command = ["pipenv", "run", "python", "./main.py", "create", "model",
               "chatgpt", "-n", model_name, "-k", "test_key", "--sub-model", "gpt-4"]

    # Act
    subprocess.run(command, cwd=cwd)
    model = JsonDataManager.load(["models", model_name], GPTWrapper)

    # Assert
    assert model.api_key == 'mock'
    assert model.model == 'gpt-4'


def test_create_flow(create_model_fixture, cwd):
    # Arrange
    flow_name = "test_flow"
    model_name = "test_model"
    prompt1 = "prompt1"
    prompt2 = "prompt2"
    command = ["pipenv", "run", "python", "./main.py", "create", "flow",
               "--name", flow_name, "--model", model_name, "-i", prompt1, prompt2]

    # Act
    subprocess.run(command, cwd=cwd)
    flow = JsonDataManager.load(["flows", flow_name], BranchingFlow)

    # Assert
    assert flow.name == flow_name
    assert flow.instructions == [prompt1, prompt2]

    assert isinstance(flow.root_model, GPTWrapper)
    assert flow.root_model.name == model_name

    assert len(flow.branched_models) == 2
    assert isinstance(flow.branched_models[0], GPTWrapper)
    assert isinstance(flow.branched_models[1], GPTWrapper)
    assert flow.branched_models[0].name == model_name
    assert flow.branched_models[1].name == model_name
