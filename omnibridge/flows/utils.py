
from typing import Dict, List

def dict_sequential_flow_to_list(flow: Dict[str, List[str]]) -> List[str]:
    # Find the starting node (the one with no outgoing edges)
    starting_node = None
    for node, adjacent_nodes in flow.items():
        if len(adjacent_nodes) == 0:
            starting_node = node
            break

    # Traverse the DAG to create a list
    flow_list = [starting_node]
    current_node = starting_node
    while len(flow_list) < len(flow):
        for node, adjacent_nodes in flow.items():
            if current_node in adjacent_nodes:
                flow_list.append(node)
                current_node = node
                break

    return flow_list
