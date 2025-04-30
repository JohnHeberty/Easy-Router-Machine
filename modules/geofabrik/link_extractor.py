from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
from typing import Any

class LinkExtractor:
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
    def __init__(self, country: str) -> None:
        self.country: str = country

    def extract(self, html: str, base_url: str) -> str:
        """
        Extracts a download link for a specific country's latest OSM or PBF 
        file from the provided HTML content.

        Args:
            html (str): The HTML content to parse for the download link.
            base_url (str): The base URL to resolve relative links.

        Returns:
            str: The full URL of the download link.

        Raises:
            ValueError: If no matching download link is found in the HTML content.
        """
        soup: BeautifulSoup = BeautifulSoup(html, "html.parser")
        for a in soup.find_all("a", href=True):
            href: str = a["href"]
            if re.search(rf'{self.country}-latest.*\.(osm|pbf)$', href, flags=re.IGNORECASE):
                return urljoin(base_url, href)
        raise ValueError("Download link not found.")
