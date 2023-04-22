from pathlib import Path
from omnibridge.cli.create.create_command_handler import add_key, add_chatgpt, add_dalle
import omnibridge.saved_data.json_data_manager

import json



def test_add_key_command(tmp_path: Path, monkeypatch):
    # Arrange
    file_path = tmp_path / ".saved_data.json"
    monkeypatch.setattr(omnibridge.saved_data.json_data_manager, "FILE_PATH", file_path)
    args = {
        'value': 'value_mock',
        'name': 'name_mock'
    }

    # Act
    add_key(args)

    with open(file_path, 'r') as f:
        saved_data = json.load(f)


    # Assert
    assert saved_data == {
        'api keys': {
            'name_mock': {
                'value': 'value_mock'
            }
        }
    }


def test_add_chatgpt_command(api_key_fixture, tmp_path: Path, monkeypatch):
    # Arrange
    file_path = tmp_path / ".saved_data.json"
    monkeypatch.setattr(omnibridge.saved_data.json_data_manager, "FILE_PATH", file_path)
    key_name = "mock_key_name"
    model_name = 'gpt_model'
    model = 1
    api_key_fixture(file_path, key_name)

    args = {
        'model': model,
        'name': model_name,
        'key': key_name,
        'sub_model': 1
    }


    # Act
    add_chatgpt(args)

    with open(file_path, 'r') as f:
        saved_data = json.load(f)


    # Assert
    assert saved_data == {
        'api keys': {
            key_name:  {
                'value': 'api_key_mock'
            }
        },
        'models': {
            model_name: {
                '_class_type': 'chat_gpt',
                'api key': 'api_key_mock',
                'model': model
            }
        }
    }

    
def test_add_dalle_command(api_key_fixture, tmp_path: Path, monkeypatch):
    # Arrange
    file_path = tmp_path / ".saved_data.json"
    monkeypatch.setattr(omnibridge.saved_data.json_data_manager, "FILE_PATH", file_path)
    key_name = "mock_key_name"
    model_name = 'dalle_model'
    num_of_images = 4
    resolution = 'mock_resolution'
    api_key_fixture(file_path, key_name)

    args = {
        'key': key_name,
        'num_images': num_of_images,
        'res': resolution,
        'name': model_name
    }

    # Act
    add_dalle(args)

    with open(file_path, 'r') as f:
        saved_data = json.load(f)

    
    # Assert
    assert saved_data == {
        'api keys': {
            key_name:  {
                'value': 'api_key_mock'
            }
        },
        'models': {
            'dalle_model': {
                '_class_type': 'dalle',
                'api key': 'api_key_mock',
                'number of images per prompt': num_of_images,
                'resolution': resolution
            }
        }
    }