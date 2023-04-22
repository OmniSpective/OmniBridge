import pytest
from pathlib import Path
from omnibridge.cli.create.create_command_handler import add_key
import omnibridge.saved_data.json_data_manager


@pytest.fixture
def api_key_fixture():
    def _save_api_key_for_tests(file_path: Path, key_name: str):
        omnibridge.saved_data.json_data_manager.FILE_PATH = file_path
        args = {
            'value': 'api_key_mock',
            'name': key_name,
        }
        add_key(args)

    return _save_api_key_for_tests