from typing import Union

import requests
from bs4 import BeautifulSoup

from omnibridge.model_entities.models_io.base_model_io import TextualIO

class WebInputHandler:
    @staticmethod
    def convert_url_page(url: str) -> Union[TextualIO, None]:
        """
        Reads the content of a .txt file given its file path.

        Args:
            file_path (str): The path to the file.

        Returns:
            TextualIO: The content of the file ready to be consumed by models.
        """
        print ('Scraping URL')
        
        # Send a GET request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Remove any script and style elements from the HTML
            for script in soup(['script', 'style']):
                script.decompose()

            # Extract the text from the HTML
            text = soup.get_text()

            # Remove any leading or trailing whitespace and join the lines
            text = '\n'.join(line.strip() for line in text.splitlines() if line.strip())

            return TextualIO(text=text)
        else:
            print(f"Failed to download the content. Status code: {response.status_code}")
            return None