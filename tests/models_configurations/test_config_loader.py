from pathlib import Path

from omnibridge.wrappers.wrapper_instance_configurations.config_types import ConfigTypes
from omnibridge.wrappers.wrapper_instance_configurations.dalle_config import DALLEConfiguration
from omnibridge.wrappers.wrapper_instance_configurations.hugging_face_config import HuggingFaceConfiguration
from omnibridge.wrappers.wrapper_instance_configurations.config_loader import parse_models_configurations_from_file


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
