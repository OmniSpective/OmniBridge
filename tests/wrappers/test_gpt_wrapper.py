import responses
import pytest

from omnibridge.wrappers.api_based_wrappers.gpt_wrapper import COMPLETIONS_API_URL, GPTWrapper, GPTWrapperException
from omnibridge.wrappers.models_configurations.chatgpt_config import GPTConfiguration


@pytest.fixture
def well_structured_response():
    return {
        "choices": [
            {
                "message": {
                    "content": "mock"
                }
            }
        ]
    }


@pytest.fixture
def bad_structured_response():
    return {
        "bad-structure": [
            {
                "mock": "mock"
            }
        ]
    }


@responses.activate
def test_gpt_wrapper(well_structured_response):
    # Arrange
    responses.add(responses.POST, COMPLETIONS_API_URL, json=well_structured_response)
    wrapper = GPTWrapper(configuration=GPTConfiguration(api_key='abc', model='gpt-4'))

    # Act
    res = wrapper.prompt('send_mock')

    # Assert
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == COMPLETIONS_API_URL
    assert res == {'response': 'mock'}


@responses.activate
def test_gpt_wrapper_fail(bad_structured_response):
    # Arrange
    responses.add(responses.POST, COMPLETIONS_API_URL, json=bad_structured_response)
    wrapper = GPTWrapper(configuration=GPTConfiguration(api_key='abc', model='gpt-4'))

    # Act
    with pytest.raises(KeyError) as exc_info:
        wrapper.prompt('send_mock')

    # Assert
    assert exc_info.value.args[0] == "choices"


@responses.activate
def test_gpt_wrapper_api_call_fails():
    # Arrange
    responses.add(responses.POST, COMPLETIONS_API_URL, json={}, status=500)
    wrapper = GPTWrapper(configuration=GPTConfiguration(api_key='abc', model='gpt-4'))

    # Act
    with pytest.raises(GPTWrapperException) as exc_info:
        wrapper.prompt('send_mock')

    # Assert
    assert str(exc_info.value) == "Request to chatgpt completions api failed due to 500 Server Error: " \
                                  "Internal Server Error for url: https://api.openai.com/v1/chat/completions. " \
                                  "\nMessage response: {}"
