import os
from typing import Union

from omnibridge.model_entities.models_io.base_model_io import TextualIO


class FileInputHandler:
    @staticmethod
    def convert_file(file_path: str) -> Union[TextualIO, None]:
        """
        Reads the content of a file given its file path.

        Args:
            file_path (str): The path to the file.

        Returns:
            TextualIO: The content of the file ready to be consumed by models.
        """

        allowed_extensions = {
            '.txt': FileInputHandler.convert_txt_file,
            '.py': FileInputHandler.convert_txt_file
        }

        _, file_extension = os.path.splitext(file_path)

        if file_extension.lower() not in allowed_extensions.keys():
            raise ValueError(f"Error: The provided file must be of the following types: {allowed_extensions.keys()}.")

        file_conversion_func = allowed_extensions[file_extension]

        return file_conversion_func(file_path)

    @staticmethod
    def convert_txt_file(file_path: str) -> TextualIO:
        """
        Reads the content of a .txt file given its file path.

        Args:
            file_path (str): The path to the file.

        Returns:
            TextualIO: The content of the file ready to be consumed by models.
        """

        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return TextualIO(content)
