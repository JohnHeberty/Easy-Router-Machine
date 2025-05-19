from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
from typing import Any

class DateExtractor:
    """
    This module provides the `LinkExtractor` class, which is used to extract download links
    for OpenStreetMap (OSM) or Protocolbuffer Binary Format (PBF) files from HTML content.
    Classes:
        LinkExtractor: A class that extracts a specific download link for a given country
        from an HTML page.
    Dependencies:
        - BeautifulSoup from bs4: Used for parsing HTML content.
        - re: Used for regular expression matching.
        - urljoin from urllib.parse: Used to construct absolute URLs from relative links.
    Exceptions:
        - ValueError: Raised when no matching download link is found in the HTML content.
    """
    def __init__(self) -> None:
        pass

    def extract(self, html: str) -> str:
        """
        Extracts a date in the specified ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ) from the given HTML content.
        Args:
            html (str): The HTML content as a string.
        Returns:
            str: The extracted date in ISO 8601 format.
        Raises:
            ValueError: If no date in the specified format is found in the HTML content.
        """
        
        soup: BeautifulSoup = BeautifulSoup(html, "html.parser")

        # Extract all text from the HTML
        text_content = soup.get_text()

        # Search for the date in the specified format
        date_pattern = r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z"
        match = re.search(date_pattern, text_content)

        if not match:
            raise ValueError("No date in the specified format found in the HTML content.")

        return match.group(0)
