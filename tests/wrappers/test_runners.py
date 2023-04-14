from omnibridge.wrappers.runners import run_prompt_in_chatgpt_wrapper
from omnibridge.wrappers.wrapper_instances.gpt_wrapper import COMPLETIONS_API_URL
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

    # Act
    res = run_prompt_in_chatgpt_wrapper(prompt="mock", api_key='mock', model='gpt-4')

    # Assert
    res == {'response': 'mock'}


@responses.activate
def test_run_chatgpt_wrapper_api_call_failed():
    # Arrange
    responses.add(responses.POST, COMPLETIONS_API_URL, json={}, status=500)

    # Act
    res = run_prompt_in_chatgpt_wrapper(prompt="mock", api_key='mock', model='gpt-4')

    # Assert
    assert res is None
