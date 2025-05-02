from .file_downloader import FileDownloader
from .link_extractor import LinkExtractor
from .page_fetcher import PageFetcher
import os

class ProtobufDownloader:
    """
    A class to handle downloading of Protobuf (.osm.pbf) files from Geofabrik.
    Attributes:
        url (str): The URL of the Geofabrik page to fetch data from.
        country (str): The country name to filter download links.
        path_folder (str): The directory path where the downloaded file will be saved.
        path_file (str): The full path of the downloaded file.
        fetcher (PageFetcher): An instance of PageFetcher to fetch HTML content.
        extractor (LinkExtractor): An instance of LinkExtractor to extract download links.
        downloader (FileDownloader): An instance of FileDownloader to handle file downloads.
    """
    def __init__(self,
            url: str        = "https://download.geofabrik.de/south-america/brazil.html",
            country: str    = "brazil",
            path_data: str  = "data",
            path_output: str= "external",
            path_module: str= "protobuf",
            timeout: int    = 10
        ):
        self.url            = url
        self.country        = country
        self.path_folder    = os.path.join(path_data, path_output, path_module)
        os.makedirs(self.path_folder, exist_ok=True)
        self.path_file      = os.path.join(self.path_folder, f"{country}-latest.osm.pbf")

        self.fetcher        = PageFetcher()
        self.extractor      = LinkExtractor(self.country)
        self.downloader     = FileDownloader(timeout=timeout)

    def run(self) -> None:
        """
        Executes the process of fetching HTML content, extracting the download URL,
        downloading the file, and saving it to the specified path.

        This method performs the following steps:
        1. Fetches the HTML content from the specified URL using the fetcher.
        2. Extracts the download URL from the HTML content using the extractor.
        3. Downloads the file from the extracted URL using the downloader.
        4. Saves the downloaded file to the specified file path.

        Prints a confirmation message upon successful download and save.

        Returns:
            None
        """
        if os.path.exists(self.path_file): 
            return self.path_file
        print(f"Baixando arquivo: {self.path_file}")
        html_content = self.fetcher.fetch(self.url)
        download_url = self.extractor.extract(html_content, self.url)
        status, path = self.downloader.download(download_url, self.path_file)
        print(f"Download concluído e salvo como {self.path_file}")
        return path if status else None
