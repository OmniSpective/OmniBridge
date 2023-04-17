import subprocess
from omnibridge.wrappers.wrapper_instances.type_name_to_wrapper import type_names


def test_list_wrappers(capsys):
    command = ["python", "./main.py", "list", "wrappers"]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    captured_output = capsys.readouterr()

    assert captured_output.out == f'{[type for type in type_names.keys()]}'
