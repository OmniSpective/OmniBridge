from typing import Dict, List
from omnibridge.flows.file_to_flow import read_flow_from_json, read_flow_from_yaml
from omnibridge.flows.flow_types import identify_dag_type, DagType

def test_json_to_dict():
    file_path = 'tests/flows/test_flows/seq_flow.json'
    flow, flow_name = read_flow_from_json(file_path=file_path)
    assert 'step1' in flow.keys()
    assert len(flow['step1']) == 0
    assert len(flow['step2']) == 1
    assert flow['step2'][0] == 'step1'

def test_yaml_to_dict():
    file_path = 'tests/flows/test_flows/seq_flow.yaml'
    flow, flow_name = read_flow_from_yaml(file_path=file_path)
    assert 'step1' in flow.keys()
    assert len(flow['step1']) == 0
    assert len(flow['step2']) == 1
    assert flow['step2'][0] == 'step1'


def test_dict_to_flow():
    pass


def test_flow_type_identification():
    file_path = 'tests/flows/test_flows/seq_flow.yaml'
    flow, flow_name = read_flow_from_yaml(file_path=file_path)
    flow_type: DagType = identify_dag_type(flow)
    assert flow_type == DagType.SEQUENTIAL


    file_path = 'tests/flows/test_flows/seq_flow.json'
    flow, flow_name = read_flow_from_json(file_path=file_path)
    flow_type: DagType = identify_dag_type(flow)
    assert flow_type == DagType.SEQUENTIAL


    file_path = 'tests/flows/test_flows/branch_flow.json'
    flow, flow_name = read_flow_from_json(file_path=file_path)
    flow_type: DagType = identify_dag_type(flow)
    assert flow_type == DagType.BRANCHING
