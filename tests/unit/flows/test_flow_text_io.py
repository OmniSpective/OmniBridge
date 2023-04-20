from omnibridge.model_entities.models_io.base_model_io import TextualIO
from omnibridge.model_entities.models_io.flow_io import FlowIO


def test_flow_text_io_succeed():
    # Arrange
    flow_io = FlowIO(TextualIO("hello"))
    model_text_io = TextualIO("world")

    # Act
    flow_io += model_text_io

    # Assert
    assert flow_io.get_text() == "hello\nworld"

