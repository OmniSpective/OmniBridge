from omnibridge.wrappers.wrapper_instances.type_name_to_wrapper import type_names


def handle_list_wrappers_command():
    for type, _ in type_names.items():
        print (f'Wrapper: {type}')