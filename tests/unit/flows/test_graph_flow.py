from omnibridge.flows.graph_flow import Node, GraphFlow
from omnibridge.model_entities.models_io.base_model_io import ModelIO, TextualIO, ImageIO
from omnibridge.wrappers.wrapper_interfaces.processor import Processor


class MockProcessor(Processor):
    processed = 0
    output = "test_output"

    def __init__(self, return_value: ModelIO = TextualIO(output)):
        self.return_value = return_value

    def process(self, model_input: ModelIO) -> ModelIO:
        MockProcessor.processed += 1
        return self.return_value


def test_single_node_graph_flow():
    # Arrange
    MockProcessor.processed = 0
    node = Node(MockProcessor())
    flow = GraphFlow([node])
    flow_input = TextualIO("test_input")

    # Act
    flow.process(flow_input)

    # Assert
    assert MockProcessor.processed == 1


def test_chained_node_graph_flow():
    # Arrange
    MockProcessor.processed = 0
    last_node = Node(MockProcessor())
    node = Node(MockProcessor(), "", [last_node])
    flow = GraphFlow([node])
    flow_input = TextualIO("test_input")

    # Act
    flow.process(flow_input)

    # Assert
    assert MockProcessor.processed == 2


def test_parallel_node_graph_flow():
    # Arrange
    MockProcessor.processed = 0
    node = Node(MockProcessor())
    flow = GraphFlow([node, node])
    flow_input = TextualIO("test_input")

    # Act
    flow.process(flow_input)

    # Assert
    assert MockProcessor.processed == 2


def test_complex_graph_flow():
    # Arrange
    MockProcessor.processed = 0
    last_nodes = Node(MockProcessor(ImageIO(["./file1", "./file2"])))
    nodes = [Node(MockProcessor(), instruction="", next_nodes=[last_nodes]) for _ in range(2)]
    flow = GraphFlow(nodes)
    flow_input = TextualIO("test_input")

    # Act
    flow.process(flow_input)

    # Assert
    assert MockProcessor.processed == 4
