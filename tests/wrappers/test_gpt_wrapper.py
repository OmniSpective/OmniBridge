import responses
import pytest

from omnibridge.model_entities.models_io.base_model_io import TextualIO
from omnibridge.wrappers.wrapper_instances.rest_api_wrapper import WrapperException
from omnibridge.wrappers.wrapper_instances.gpt_wrapper import COMPLETIONS_API_URL, GPTWrapper


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
    wrapper = GPTWrapper(name='testgpt', api_key='abc', model='gpt-4')

    # Act
    res = wrapper.process(TextualIO('send_mock'))

    # Assert
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == COMPLETIONS_API_URL
    assert res.text == 'mock'


@responses.activate
def test_gpt_wrapper_fail(bad_structured_response):
    # Arrange
    responses.add(responses.POST, COMPLETIONS_API_URL, json=bad_structured_response)
    wrapper = GPTWrapper(name='testgpt', api_key='abc', model='gpt-4')

    # Act
    with pytest.raises(KeyError) as exc_info:
        wrapper.process(TextualIO('send_mock'))

    # Assert
    assert exc_info.value.args[0] == "choices"


@responses.activate
def test_gpt_wrapper_api_call_fails():
    # Arrange
    responses.add(responses.POST, COMPLETIONS_API_URL, json={}, status=500)
    wrapper = GPTWrapper(name='testgpt', api_key='abc', model='gpt-4')

    # Act
    with pytest.raises(WrapperException) as exc_info:
        wrapper.process(TextualIO('send_mock'))

    # Assert
    assert str(exc_info.value).startswith(f"Request to api endpoint: {COMPLETIONS_API_URL} failed.")
