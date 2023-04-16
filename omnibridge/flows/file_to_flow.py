import json
import yaml

from typing import Dict, List, Tuple

# require - pip install pyyaml


def read_flow_from_json(file_path: str) -> Tuple[Dict[str, List[str]], str]:
    with open(file_path, 'r') as json_file:
        json_data = json.load(json_file)

    flow_name = json_data['name']
    flow = {}
    for node, node_info in json_data['steps'].items():
        flow[node] = node_info["depends_on"]

    return flow, flow_name

def read_flow_from_yaml(file_path: str) -> Tuple[Dict[str, List[str]], str]:
    with open(file_path, 'r') as yaml_file:
        yaml_data = yaml.safe_load(yaml_file)

    flow_name = yaml_data["name"]
    flow = {}
    for node, node_info in yaml_data["steps"].items():
        flow[node] = node_info["depends_on"]

    return flow, flow_name

