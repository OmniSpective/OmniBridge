from enum import Enum
from typing import Dict, List

class DagType(str, Enum):
    SEQUENTIAL = "sequential"
    BRANCHING = "brnaching"

def is_sequential(dag: Dict[str, List[str]]) -> bool:
    node_outgoing_edges = [len(adjacent_nodes) for adjacent_nodes in dag.values()]
    zero_outgoing_count = node_outgoing_edges.count(0)
    one_outgoing_count = node_outgoing_edges.count(1)

    return zero_outgoing_count == 1 and one_outgoing_count == len(dag) - 1

def is_branching(dag: Dict[str, List[str]]) -> bool:
    node_outgoing_edges = [len(adjacent_nodes) for adjacent_nodes in dag.values()]
    zero_outgoing_count = node_outgoing_edges.count(0)
    one_outgoing_count = node_outgoing_edges.count(1)

    return zero_outgoing_count == len(dag) - 1 and one_outgoing_count == 1


def identify_dag_type(dag: Dict[str, List[str]]) -> DagType:
    if is_sequential(dag):
        return DagType.SEQUENTIAL
    elif is_branching(dag):
        return DagType.BRANCHING
    else:
        raise NotImplementedError('The following Flow structure is not supported yet')
