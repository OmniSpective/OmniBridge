import pytest
from pathlib import Path
from omnibridge.cli.argument_parser.commands import add_key


@pytest.fixture
def api_key_fixture():
    def _save_api_key_for_tests(file_path: Path, key_name: str):
        args = {
            'value': 'api_key_mock',
            'name': key_name
        }
        add_key(args, file_path)

    return _save_api_key_for_tests