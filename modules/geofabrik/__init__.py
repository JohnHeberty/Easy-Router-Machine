from .file_downloader import FileDownloader
from .link_extractor import LinkExtractor
from .page_fetcher import PageFetcher
from .date_extractor import DateExtractor
import json
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
            path_module: str= "pbf",
            timeout: int    = 10
        ):
        self.url            = url
        self.country        = country
        self.path_folder    = os.path.join(path_data, path_output, path_module)
        os.makedirs(self.path_folder, exist_ok=True)
        self.path_file      = os.path.join(self.path_folder, f"{country}-latest.osm.pbf")

        self.fetcher        = PageFetcher()
        self.dtextract      = DateExtractor()
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
        date_save               = ""
        name_data               = f"{os.path.basename(self.path_file)}.json"
        if os.path.exists(self.path_file):
            if os.path.exists(name_data):
                with open(name_data, "r", encoding="utf-8") as file:
                    date_save   = json.load(file)
        html_content            = self.fetcher.fetch(self.url)
        date_now                = self.dtextract.extract(html_content)
        if date_now != date_save:
            print(f"Baixando arquivo: {self.path_file}")
            download_url = self.extractor.extract(html_content, self.url)
            status, path = self.downloader.download(download_url, self.path_file)
            if status:
                with open(name_data, "w", encoding="utf-8") as file:
                    json.dump(date_now, file, ensure_ascii=False, indent=4)
                print(f"Download concluído e salvo como {self.path_file}")
            else:
                print(f"Erro ao baixar o arquivo: {self.path_file}")
            return path if status else None
        else:
            print(f"Arquivo já existe: {self.path_file}")
            return self.path_file
