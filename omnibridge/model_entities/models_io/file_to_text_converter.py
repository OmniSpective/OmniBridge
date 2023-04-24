import os
import pypdf
from typing import Union, Optional, List


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
            '.py': FileInputHandler.convert_txt_file,
            '.pdf': FileInputHandler.convert_pdf_file
        }

        _, file_extension = os.path.splitext(file_path)

        if file_extension.lower() not in allowed_extensions.keys():
            raise ValueError(f"Error: The provided file must be of the following types: {allowed_extensions.keys()}.")

        file_conversion_func = allowed_extensions[file_extension]

        return file_conversion_func(file_path)

    @staticmethod
    def convert_txt_file(file_path: str) -> Union[List[TextualIO], TextualIO]:
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

    @staticmethod
    def convert_pdf_file(file_path: str, divide_to_pages: Optional[bool] = False) -> Union[List[TextualIO], TextualIO]:
        """
        Reads the content of a .txt file given its file path.

        Args:
            file_path (str): The path to the file.

        Returns:
            TextualIO: The content of the file ready to be consumed by models.
        """
        print ('Loading PDF')
        # pdf_reader = pypdf.PdfReader(file_path)
        # pages = [TextualIO(text=page.extract_text()) for page in pdf_reader.pages]

        # if divide_to_pages:
        #     return pages
        
        # overall_document = ""
        # for page in pages:
        #     overall_document += (page.text + '\n')
        # return TextualIO(text=overall_document)

        from pdfminer.high_level import extract_text

        text = extract_text(file_path)
        return TextualIO(text=text)