from omnibridge.wrappers.runners import run_chatgpt_wrapper
from omnibridge.wrappers.api_based_wrappers.gpt_wrapper import COMPLETIONS_API_URL
from omnibridge.wrappers.models_configurations.chatgpt_config import GPTConfiguration
import responses
import pytest


@pytest.fixture
def gpt_response():
    return {
        "choices": [
            {
                "message": {
                    "content": "mock"
                }
            }
        ]
    }


@responses.activate
def test_run_chatgpt_wrapper(gpt_response):
    # Arrange
    responses.add(responses.POST, COMPLETIONS_API_URL, json=gpt_response)
    config = GPTConfiguration(api_key='mock', model='gpt-4')

    # Act
    res = run_chatgpt_wrapper(prompt="mock", config=config)

    # Assert
    res == {'response': 'mock'}


@responses.activate
def test_run_chatgpt_wrapper_api_call_failed():
    # Arrange
    responses.add(responses.POST, COMPLETIONS_API_URL, json={}, status=500)
    config = GPTConfiguration(api_key='mock', model='gpt-4')

    # Act
    res = run_chatgpt_wrapper(prompt="mock", config=config)

    # Assert
    assert res is None