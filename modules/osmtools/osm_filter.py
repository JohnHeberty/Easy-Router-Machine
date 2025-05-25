from glob import glob
import subprocess
import platform
import time
import os

class OSMfilter:
    """
    OSMfilter is a class designed to filter OpenStreetMap (OSM) data based on specified categories 
    and attributes. It provides functionality to configure the binary file used for filtering, 
    set input and output file paths, and execute the filtering process.
        base_path (str): The base directory for the module.
        folder_module (str): The folder name of the module.
        folder_bin (str): The folder name containing binary files.
        base_sys (str): The operating system name (e.g., Windows, Linux).
        base_name (str): The base name of the binary file.
        path_bin (str): The full path to the binary folder.
        file_bin (str): The selected binary file for filtering.
        files_bin (list): A list of available binary files in the binary folder.
        categories_viarias_unicas (list): A list of unique road categories for filtering.
        base_categories (list): A list of base attributes required for processing.
        base_data (str): The base directory for data files.
        processed (str): The folder name for processed files.
        folder_in_data (str): The directory for input data files.
    Methods:
        input_file (property):
            Getter and setter for the input file path. Ensures the file exists in the 
            specified directory and sets the corresponding output file path.
        run():
            Executes a subprocess command to filter OSM data. Constructs the command-line 
            arguments, validates attributes, and runs the binary file with the input and 
            output files. Appends filtering options for road categories and unique road 
            categories. Measures and prints the processing time along with the command output.
        TypeError: If the input file name is not a string.
        FileExistsError: If the input file does not exist in the specified directory.
        subprocess.CalledProcessError: If the subprocess command fails during execution.
    """
    def __init__(self, verbose: bool = False):
        
        self.verbose            = verbose

        # BASE PATH MODULE
        self.base_path          = "modules"
        self.folder_module      = "osmtools"
        self.folder_bin         = "bin"
        self.base_sys           = platform.system()
        self.base_name          = "osmfilter"
        self.path_bin           = os.path.join(
            self.base_path, 
            self.folder_module, 
            self.folder_bin, 
            self.base_sys, 
            self.base_name 
        )

        # ESCOLHENDO BINARIO DE CONVERSÃO
        self.file_bin           = ""
        self.files_bin          = glob(os.path.join(self.path_bin, self.base_name+"*"))
        if self.files_bin.__len__() == 1:
            self.file_bin       = self.files_bin[0]
        else:
            matching_bins   = [b for b in self.files_bin if "32" in b]
            self.file_bin = matching_bins[0] if matching_bins else self.files_bin[0]
            del(matching_bins)

        # BASE PATH FILES
        self.base_data          = "data"

        # BASE PATH OUT FILES
        self.processed          = "processed"
        self.folder_in_data     = os.path.join(self.base_data, self.processed, "o5m")
        os.makedirs(self.folder_in_data, exist_ok=True)

        self.args               = []

    @property
    def input_file(self) -> str:
        """
        Return the input file path.

        This method returns the path of the input file that has been set for the instance.
        The path is returned as a string.

        Returns:
            str: The file path assigned to the input file.
        """
        return self._input_file

    @input_file.setter
    def input_file(self, name: str) -> None:
        if not isinstance(name, str):
            raise TypeError("input_file must be a string")
        path = os.path.join(self.folder_in_data, name)
        if os.path.exists(path):
            self._input_file = path
            self._output_file = os.path.join(self.folder_in_data, os.path.splitext(name)[0] + ".filtered.streets.o5m")
        else:
            raise FileExistsError(f"input_file not exists in {self.folder_in_data}")

    def run(self):
        """
        Executes a subprocess command to filter OpenStreetMap (OSM) data based on specified categories.
        This method constructs a command-line argument list, validates attributes, and runs the 
        specified binary file with the provided input and output files. It also appends filtering 
        options for road categories and unique road categories.
        Attributes:
            self.file_bin (str): The binary file to execute.
            self._input_file (str): The input file containing OSM data.
            self.base_categories (list): A list of base categories for filtering.
            self.categories_viarias_unicas (list): A list of unique road categories for filtering.
            self._output_file (str): The output file to save the filtered data.
        Steps:
            1. Constructs the argument list for the subprocess command.
            2. Appends filtering options for categories.
            3. Defines the output file.
            4. Executes the subprocess command and captures its output.
            5. Measures and prints the processing time along with the command output.
        Raises:
            subprocess.CalledProcessError: If the subprocess command fails.
        """

        # Constroi a lista de argumentos com validação dos atributos
        self.file_bin = f"./{self.file_bin}" if self.base_sys == "Linux" else self.file_bin
        self.args = [self.file_bin, self._input_file]

        # MANTEM A TAG PRINCIPAL
        self.args.append("--keep=highway=") # waterway=

        # Define o arquivo de saída
        self.args.append(f"-o={self._output_file}")

        # Executa o comando formado
        t_start     = time.time()
        result      = subprocess.run(self.args, capture_output=True, text=True, check=True)
        t_current   = time.time() - t_start
        if self.verbose:
            print(f"Tempo do Processamento: {t_current}s")

        stdout      = result.stdout
        stderr      = result.stderr

        if stderr != "" and self.verbose:
            print("ERROR: ", stderr)
            return False
        if stdout != "" and self.verbose:
            print("Result: ", stdout)
            return True

