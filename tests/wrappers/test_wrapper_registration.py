import logging
import pytest

from omnibridge.wrappers.wrapper_instances.type_name_to_wrapper import type_names, register_wrapper


def test_wrapper_registration():
    @register_wrapper
    class TestWrapper:

        @classmethod
        def get_class_type_field(cls) -> str:
            return "test_wrapper"
    assert 'test_wrapper' in type_names.keys()
