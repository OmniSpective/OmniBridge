from omnibridge.model_entities.models_io.base_model_io import FlowTextIO, TextualIO


def test_flow_text_io_succeed():
    # Arrange
    flow_io = FlowTextIO("hello")
    model_text_io = TextualIO("world")

    # Act
    flow_io += model_text_io

    # Assert
    assert flow_io.get_text() == "hello\nworld"

