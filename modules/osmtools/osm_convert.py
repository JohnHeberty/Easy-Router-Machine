from glob import glob
import subprocess
import platform
import psutil
import time
import math
import os

class OSMConvert:
    """
    OSMConvert
    This class provides an interface for converting OpenStreetMap (OSM) data using an external binary
    conversion tool. Depending on the system’s memory, it selects between a 32-bit or 64-bit binary and 
    configures the necessary execution parameters.
    Initialization:
        OSMConvert(minimal_ram: int = 4)
            minimal_ram: An integer representing the minimum RAM in GB required to run the 64-bit binary.
                         If system memory (in GB) is less than or equal to this value, a 32-bit binary will be used.
    Attributes:
        base_name (str):
            The base name for the conversion binary.
        base_path (str):
            The root folder for the modules.
        folder_module (str):
            The name of the module folder.
        folder_bin (str):
            The subfolder containing the binary executable.
        base_sys (str):
            The operating system name as returned by the platform.
        folder_bits (str):
            A folder name determined by the system architecture (e.g., "64bits" or "32bits").
        path_protobufs (str):
            The path to the external protobuf data folder.
        path_bin (str):
            The full path to the binary based on system information and configuration.
        file_bin (str):
            The specific binary file chosen for the conversion based on matching conditions and system RAM.
        ram_system (int):
            The total RAM (in GB) of the current system.
        base_data (str):
            The base directory for data files.
        protobufs (str):
            The folder name for protobuf files.
        external (str):
            The folder used for external data.
        folder_in_data (str):
            The complete path to the input data directory.
        processed (str):
            The folder name for processed (output) data.
        folder_out_data (str):
            The complete path to the output data directory.
    Properties:
        input_file (str):
            A property to get or set the input file path. The setter verifies that the file exists under 
            the expected input directory.
        drop_author (bool):
            A flag indicating whether the author information should be dropped; must be a boolean.
        drop_version (bool):
            A flag indicating whether the version information should be dropped; must be a boolean.
        verbose (bool):
            A flag to enable verbose mode; must be a boolean.
        complete_ways (bool):
            A flag to determine if complete ways should be processed; must be a boolean.
        complete_multipolygons (bool):
            A flag to determine if complete multipolygon ways should be processed; must be a boolean.
        max_objects (int):
            Specifies the maximum number of objects to process; must be an integer.
        hash_memory (int):
            Specifies the memory allocated for hash operations; must be an integer.
        output_file (str):
            A property to get or set the output file path. The setter validates that the designated output 
            directory exists.
    Methods:
        run():
            Constructs the command-line arguments based on the current configuration and selected properties,
            then executes the binary conversion tool as a subprocess.
            It captures and prints the output along with the processing time.
    Exceptions:
        TypeError:
            Raised by setter methods when the provided value does not match the expected type.
        FileExistsError:
            Raised when expected input files or directories do not exist.
    """
    
    def __init__(self, minimal_ram: int = 4):
        
        # BASE PATH MODULE
        self.base_name          = "osmconvert"
        self.base_path          = "modules"
        self.folder_module      = "osmtools"
        self.folder_bin         = "bin"
        self.base_sys           = platform.system()
        self.folder_bits        = f"{''.join([a for a in platform.architecture()[0] if a.isdigit()])}bits"
        self.protobufs          = "protobuf"
        self.path_protobufs     = os.path.join("data","external",self.protobufs)
        self.path_bin           = os.path.join(
            self.base_path, 
            self.folder_module, 
            self.folder_bin, 
            self.base_sys, 
            self.base_name, 
            self.folder_bits
        )
        
        # CONDIÇÃO DE AJUSTE DE BINARIOS PARA NÃO SOBRECARREGAR A RAM
        self.ram_system         = math.ceil(psutil.virtual_memory().total / (1024**3))
        if self.ram_system <= minimal_ram:
            self.path_bin       = self.path_bin.replace("64bits","32bits")
        
        # ESCOLHENDO BINARIO DE CONVERSÃO
        self.file_bin           = ""
        self.files_bin          = glob(os.path.join(self.path_bin, self.base_name+"*"))
        if self.files_bin.__len__() == 1:
            self.file_bin       = self.files_bin[0]
        else:
            if self.ram_system <= minimal_ram: # CASO RAM FOR MENOR QUE 4 E MINIMAL ESTIVER DISPONIVEL USE
                matching_bins   = [b for b in self.files_bin if "minimal" in b]
            else:
                matching_bins   = [b for b in self.files_bin if "minimal" not in b]
            self.file_bin = matching_bins[0] if matching_bins else self.files_bin[0]
            del(matching_bins)

        # BASE PATH FILES
        self.base_data          = "data"

        # BASE PATH IN FILES
        self.external           = "external"
        self.folder_in_data     = os.path.join(self.base_data, self.external, self.protobufs)
        os.makedirs(self.folder_in_data, exist_ok=True)
    
        # BASE PATH OUT FILES
        self.processed          = "processed"
        self.folder_out_data    = os.path.join(self.base_data, self.processed, "o5m")
        os.makedirs(self.folder_out_data, exist_ok=True)

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
            self._output_file = os.path.join(self.folder_out_data, os.path.splitext(name)[0] + ".o5m")
        else:
            raise FileExistsError(f"input_file not exists in {self.folder_in_data}")

    @property
    def drop_author(self) -> bool:
        """
        Determines whether author information should be omitted.

        Returns:
            bool: True if author information is to be dropped, False otherwise.
        """
        return self._drop_author

    @drop_author.setter
    def drop_author(self, flag: bool) -> None:
        if not isinstance(flag, bool):
            raise TypeError("drop_author must be a boolean")
        self._drop_author = flag

    @property
    def drop_version(self) -> bool:
        """
        Indicates whether the version should be dropped.

        Returns:
            bool: True if the version is to be dropped, otherwise False.
        """
        return self._drop_version

    @drop_version.setter
    def drop_version(self, flag: bool) -> None:
        if not isinstance(flag, bool):
            raise TypeError("drop_version must be a boolean")
        self._drop_version = flag

    @property
    def verbose(self) -> bool:
        """
        Return whether verbose mode is enabled.

        Returns:
            bool: True if verbose mode is enabled, False otherwise.
        """
        return self._verbose

    @verbose.setter
    def verbose(self, flag: bool) -> None:
        if not isinstance(flag, bool):
            raise TypeError("verbose must be a boolean")
        self._verbose = flag

    @property
    def complete_ways(self) -> bool:
        """
        Indicates whether the ways are complete.

        Returns:
            bool: True if the ways are complete, False otherwise.
        """
        return self._complete_ways

    @complete_ways.setter
    def complete_ways(self, flag: bool) -> None:
        if not isinstance(flag, bool):
            raise TypeError("complete_ways must be a boolean")
        self._complete_ways = flag

    @property
    def complete_multipolygons(self) -> bool:
        """
        Return whether multipolygons are complete.

        Returns:
            bool: True if multipolygons are complete; False otherwise.
        """
        return self._complete_multipolygons

    @complete_multipolygons.setter
    def complete_multipolygons(self, flag: bool) -> None:
        if not isinstance(flag, bool):
            raise TypeError("complete_multipolygons must be a boolean")
        self._complete_multipolygons = flag

    @property
    def max_objects(self) -> int:
        """
        Return the maximum number of objects allowed.

        Returns:
            int: The maximum number of objects.
        """
        return self._max_objects

    @max_objects.setter
    def max_objects(self, objects: int) -> None:
        if not isinstance(objects, int):
            raise TypeError("max_objects must be an integer")
        self._max_objects = objects

    @property
    def hash_memory(self) -> int:
        """
        Return the stored memory hash value.

        Returns:
            int: The hash representing the memory state of the object.
        """
        return self._hash_memory

    @hash_memory.setter
    def hash_memory(self, ram: int) -> None:
        if not isinstance(ram, int):
            raise TypeError("hash_memory must be an integer")
        self._hash_memory = ram

    def run(self):
        """
        Executes an external command by constructing and running a list of command-line arguments.
        This method performs the following steps:
        1. Builds an argument list starting with the binary (prefixed by "./") and the input file.
        2. Appends boolean command-line flags (e.g., --drop-author, --drop-version, --verbose, 
            --complete-ways, --complete-multipolygons)
            if the corresponding instance attributes are present and True.
        3. Appends numeric options for max objects and hash memory if these attributes are defined.
        4. Specifies the output file using the "-o=" option.
        5. Executes the command using subprocess.run, capturing any stdout and stderr.
        6. Measures the execution time and prints the command output along with the processing time.
        Raises:
             subprocess.CalledProcessError: If the subprocess execution fails (i.e., returns a 
             non-zero exit status).
        """
        # Constroi a lista de argumentos com validação dos atributos
        self.file_bin = f"./{self.file_bin}" if self.base_sys == "Linux" else self.file_bin
        self.args = [self.file_bin, self._input_file]

        # Para opções booleanas, incluímos o parâmetro somente se existir e for True.
        if hasattr(self, "_drop_author") and self._drop_author:
            self.args.append("--drop-author")
        if hasattr(self, "_drop_version") and self._drop_version:
            self.args.append("--drop-version")
        if hasattr(self, "_verbose") and self._verbose:
            self.args.append("--verbose")
        if hasattr(self, "_complete_ways") and self._complete_ways:
            self.args.append("--complete-ways")
        if hasattr(self, "_complete_multipolygons") and self._complete_multipolygons:
            self.args.append("--complete-multipolygons")

        # Para opções numéricas, incluímos o parâmetro se estiver definido.
        if hasattr(self, "_max_objects"):
            self.args.append(f"--max-objects={self._max_objects}")
        if hasattr(self, "_hash_memory"):
            self.args.append(f"--hash-memory={self._hash_memory}")

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

# OSMC = OSMConvert()

# OSMC.input_file             = 'brazil-latest.osm.pbf'
# OSMC.drop_author            = True
# OSMC.drop_version           = True
# OSMC.verbose                = True
# OSMC.complete_ways          = True
# OSMC.complete_multipolygons = True
# OSMC.max_objects            = 500000000
# OSMC.hash_memory            = 4096
# OSMC.output_file            = 'brazil-latest.osm.pbf'

# OSMC.run()