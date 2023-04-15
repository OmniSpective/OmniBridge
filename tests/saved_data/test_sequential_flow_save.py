import os

from omnibridge.flows.branching_flow import BranchingFlow
from omnibridge.flows.sequential_flow import SequentialFlow
import omnibridge.saved_data.json_data_manager
from omnibridge.saved_data.json_data_manager import JsonDataManager, MODULE_DIR
from omnibridge.wrappers.wrapper_instances.gpt_wrapper import GPTWrapper

TEST_FILE_NAME = ".saved_data_test.json"
TEST_FILE_PATH = os.path.join(MODULE_DIR, TEST_FILE_NAME)
omnibridge.saved_data.json_data_manager.FILE_PATH = TEST_FILE_PATH


def test_save_flow_succeed():
    # Arrange
    gpt = GPTWrapper("gpt3.5", api_key="fake_fake", model="gpt-3.5-turbo")
    JsonDataManager.save(["models", gpt.name], gpt)
    flow = SequentialFlow(name="myflow", models=[gpt])

    # Act
    JsonDataManager.save(["flows", flow.name], flow)
    loaded_flow: SequentialFlow = JsonDataManager.load(["flows", flow.name], SequentialFlow)

    # Assert
    model_original = flow.models[0]
    model_loaded = loaded_flow.models[0]
    assert isinstance(model_loaded, GPTWrapper)
    assert model_loaded.name == model_original.name
    assert model_loaded.model == model_original.model
    assert model_loaded.api_key == model_original.api_key


def test_save_flow_with_two_models_succeed():
    # Arrange
    gpt = GPTWrapper("gpt3.5", api_key="fake_fake", model="gpt-3.5-turbo")
    JsonDataManager.save(["models", gpt.name], gpt)
    flow = SequentialFlow(name="myflow", models=[gpt, gpt])

    # Act
    JsonDataManager.save(["flows", flow.name], flow)
    loaded_flow: SequentialFlow = JsonDataManager.load(["flows", flow.name], SequentialFlow)

    # Assert
    model_original = flow.models[0]
    model_original_2 = flow.models[1]
    model_loaded = loaded_flow.models[0]
    model_loaded_2 = loaded_flow.models[1]
    assert isinstance(model_loaded, GPTWrapper) and isinstance(model_loaded_2, GPTWrapper)
    assert model_loaded.name == model_original.name and model_loaded.model == model_original.model\
           and model_loaded.api_key == model_original.api_key
    assert model_loaded_2.name == model_original_2.name and model_loaded_2.model == model_original_2.model\
           and model_loaded_2.api_key == model_original_2.api_key


def test_save_branching_flow_succeed():
    # Arrange
    gpt = GPTWrapper("gpt3.5", api_key="fake_fake", model="gpt-3.5-turbo")
    JsonDataManager.save(["models", gpt.name], gpt)
    flow = BranchingFlow(name="myflow", root_model=gpt, branched_models=[gpt, gpt, gpt],
                         branched_instructions=["expand point 1", "expand point 2", "expand point 3"])

    # Act
    JsonDataManager.save(["flows", flow.name], flow)
    loaded_flow: BranchingFlow = JsonDataManager.load(["flows", flow.name], BranchingFlow)

    # Assert
    assert flow.instructions == loaded_flow.instructions
