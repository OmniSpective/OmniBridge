import pytest
from pathlib import Path
from omnibridge.cli.argument_parser.commands import add_key


@pytest.fixture
def api_key_fixture():
    def _save_api_key_for_tests(file_path: Path, key_name: str):
        args = {
            'value': 'api_key_mock',
            'name': key_name,
            'saved_data_file_path': file_path
        }
        add_key(args)

    return _save_api_key_for_tests