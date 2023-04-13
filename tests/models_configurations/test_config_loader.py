from pathlib import Path

from omnibridge.wrappers.wrapper_instance_configurations.config_types import ConfigTypes
from omnibridge.wrappers.wrapper_instance_configurations.chatgpt_config import GPTConfiguration
from omnibridge.wrappers.wrapper_instance_configurations.dalle_config import DALLEConfiguration
from omnibridge.wrappers.wrapper_instance_configurations.hugging_face_config import HuggingFaceConfiguration
from omnibridge.wrappers.wrapper_instance_configurations.config_loader import parse_models_configurations_from_file


def test_parse_models_configurations_from_file_chatgpt_good_config():
    # Arrange
    config_file_path = Path(__file__).parent / 'data/chatgpt/good_chatgpt_config.json'

    # Act
    result = parse_models_configurations_from_file(config_file_path)

    # Assert
    assert ConfigTypes.CHATGPT.lower() in result.keys()
    gpt_result = result[ConfigTypes.CHATGPT.lower()]
    assert isinstance(gpt_result, GPTConfiguration)
    assert gpt_result.api_key == "mock"
    assert gpt_result.model == "mock"


def test_parse_models_configurations_from_file_chatgpt_bad_config():
    # Arrange
    config_file_path = Path(__file__).parent / 'data/chatgpt/bad_chatgpt_config.json'

    # Act
    result = parse_models_configurations_from_file(config_file_path)

    # Assert
    assert ConfigTypes.CHATGPT.lower() not in result.keys()


def test_parse_models_configurations_from_file_dalle_good_config():
    # Arrange
    config_file_path = Path(__file__).parent / 'data/dalle/good_dalle_config.json'

    # Act
    result = parse_models_configurations_from_file(config_file_path)

    # Assert
    assert ConfigTypes.DALLE.lower() in result.keys()
    dalle_result = result[ConfigTypes.DALLE.lower()]
    assert isinstance(dalle_result, DALLEConfiguration)
    assert dalle_result.api_key == "mock"
    assert dalle_result.num_of_images == 1
    assert dalle_result.resolution == "mock"


def test_parse_models_configurations_from_file_dalle_bad_config():
    # Arrange
    config_file_path = Path(__file__).parent / 'data/dalle/bad_dalle_config.json'

    # Act
    result = parse_models_configurations_from_file(config_file_path)

    # Assert
    assert ConfigTypes.DALLE.lower() not in result.keys()


def test_parse_models_configurations_from_file_hugging_face_good_config():
    # Arrange
    config_file_path = Path(__file__).parent / 'data/hugging_face/good_hugging_face_config.json'

    # Act
    result = parse_models_configurations_from_file(config_file_path)

    # Assert
    assert ConfigTypes.HUGGINGFACE.lower() in result.keys()
    hugging_face_result = result[ConfigTypes.HUGGINGFACE.lower()]
    assert isinstance(hugging_face_result, HuggingFaceConfiguration)
    assert hugging_face_result.api_key == "mock"
    assert hugging_face_result.model_id == "mock"


def test_parse_models_configurations_from_file_hugging_face_bad_config():
    # Arrange
    config_file_path = Path(__file__).parent / 'data/hugging_face/bad_hugging_face_config.json'

    # Act
    result = parse_models_configurations_from_file(config_file_path)

    # Assert
    assert ConfigTypes.HUGGINGFACE.lower() not in result.keys()


def test_parse_models_configurations_from_file_good_multi_config():
    # Arrange
    config_file_path = Path(__file__).parent / 'data/multi_config/good_multi_config.json'

    # Act
    result = parse_models_configurations_from_file(config_file_path)

    # Assert
    assert ConfigTypes.CHATGPT.lower() in result.keys()
    assert ConfigTypes.DALLE.lower() in result.keys()
    assert ConfigTypes.HUGGINGFACE.lower() in result.keys()

    chatgpt_result = result[ConfigTypes.CHATGPT.lower()]
    dalle_result = result[ConfigTypes.DALLE.lower()]
    hugging_face_result = result[ConfigTypes.HUGGINGFACE.lower()]

    assert isinstance(chatgpt_result, GPTConfiguration)
    assert isinstance(dalle_result, DALLEConfiguration)
    assert isinstance(hugging_face_result, HuggingFaceConfiguration)

    assert chatgpt_result.api_key == "mock"
    assert chatgpt_result.model == "mock"

    assert dalle_result.api_key == "mock"
    assert dalle_result.num_of_images == 1
    assert dalle_result.resolution == "mock"

    assert hugging_face_result.api_key == "mock"
    assert hugging_face_result.model_id == "mock"