import responses

from omnibridge.cli.run.run_command_handler import handle_run_command
from omnibridge.wrappers.wrapper_instances.gpt_wrapper import COMPLETIONS_API_URL


@responses.activate
def test_run_model(create_model_fixture, mock_chatgpt_response, capsys):
    # Arrange
    model_name = "test_model"
    responses.add(responses.POST, COMPLETIONS_API_URL, json=mock_chatgpt_response)
    args = {
        'object_to_run': 'model',
        'name': model_name,
        'prompt': 'test_prompt'
    }

    # Act
    handle_run_command(args)
    captured = capsys.readouterr()

    # Assert
    assert captured.out == "mock\n"


@responses.activate
def test_run_flow(create_flow_fixture, mock_chatgpt_response, capsys):
    # Arrange
    flow_name = "test_flow"
    responses.add(responses.POST, COMPLETIONS_API_URL, json=mock_chatgpt_response)
    args = {
        'object_to_run': 'flow',
        'name': flow_name,
        'prompt': 'test_prompt'
    }

    # Act
    handle_run_command(args)
    captured = capsys.readouterr()

    # Assert
    assert captured.out == "mock\nmock\nmock\n"
