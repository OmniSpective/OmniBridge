import responses
import pytest

from omnibridge.wrappers.api_based_wrappers.hugging_face_wrapper import HUGGING_FACE_BASE_URL, HuggingFaceWrapper
from omnibridge.wrappers.models_configurations.hugging_face_config import HuggingFaceConfiguration
from omnibridge.wrappers.api_based_wrappers.base_api_wrapper import WrapperException


@responses.activate
def test_hugging_face_wrapper():
    # Arrange
    model_id = 'mock'
    responses.add(responses.POST, f"{HUGGING_FACE_BASE_URL}/{model_id}", json={'mock': 'mock'})
    wrapper = HuggingFaceWrapper(configuration=HuggingFaceConfiguration(api_key='abc', model_id=model_id))

    # Act
    res = wrapper.prompt('send_mock')

    # Assert
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == f"{HUGGING_FACE_BASE_URL}/{model_id}"
    assert res == {'mock': 'mock'}


@responses.activate
def test_gpt_wrapper_api_call_fails():
    # Arrange
    model_id = 'mock'
    responses.add(responses.POST, f"{HUGGING_FACE_BASE_URL}/{model_id}", json={}, status=500)
    wrapper = HuggingFaceWrapper(configuration=HuggingFaceConfiguration(api_key='abc', model_id=model_id))

    # Act
    with pytest.raises(WrapperException) as exc_info:
        wrapper.prompt('send_mock')

    # Assert
    assert str(exc_info.value).startswith("Request to api endpoint: ")
