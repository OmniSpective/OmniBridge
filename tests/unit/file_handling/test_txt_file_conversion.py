import os

from omnibridge.model_entities.models_io.file_to_text_converter import FileInputHandler


def test_txt_file_conversion_to_textual_io():
    # Arrange
    content = 'Hello, World!'
    file_name = 'hello_for_test.txt'
    with open(file_name, 'w') as f:
        f.write(content)

    # Act
    text_io = FileInputHandler.convert_file(file_name)
    os.remove(file_name)  # cleanup

    # Assert
    assert text_io.get_text() == content


def test_py_file_conversion_to_textual_io():
    content = 'print("Hello, World!")'
    file_name = 'hello_for_test.py'
    with open(file_name, 'w') as f:
        f.write(content)

    # Act
    text_io = FileInputHandler.convert_file(file_name)
    os.remove(file_name)  # cleanup

    # Assert
    assert text_io.get_text() == content
