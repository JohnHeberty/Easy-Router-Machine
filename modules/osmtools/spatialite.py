"""
Módulo para integração com os executáveis Spatialite.
Cria uma classe para cada .exe em spatialite/tools, seguindo SOLID.
"""
import subprocess
import os
# from modules.logger.logger_factory import LoggerFactory

TOOLS_PATH = os.path.join(# os.path.dirname(__file__)
    "modules", "osmtools", "bin", "Windows", "spatialite", "tools"
)

class SpatialiteBase:
    """
    Classe base para execução de binários spatialite.
    """
    def __init__(self, exe_name: str):
        """
        Inicializa a classe base com o caminho do executável e configura o logger.
        Args:
            exe_name (str): Nome do arquivo executável (.exe) a ser utilizado.
        Raises:
            FileNotFoundError: Se o executável não for encontrado no caminho esperado.
        """
        self.exe_path = os.path.join(TOOLS_PATH, exe_name)
        # self.logger = LoggerFactory().get_logger(self.__class__.__name__)
        if not os.path.exists(self.exe_path):
            raise FileNotFoundError(f"Executable not found: {self.exe_path}")

    def run(self, args: list, capture_output=True, check=True, **kwargs):
        """
        Executa o binário com os argumentos fornecidos via subprocess.
        Args:
            args (list, opcional): Lista de argumentos para passar ao executável.
            capture_output (bool, opcional): Se True, captura stdout/stderr.
            check (bool, opcional): Se True, lança exceção em erro de execução.
            **kwargs: Parâmetros adicionais para subprocess.run.
        Returns:
            subprocess.CompletedProcess: Resultado da execução do subprocess.
        Raises:
            subprocess.CalledProcessError: Se o comando retornar código 
            diferente de zero e check=True.
        """
        cmd = [self.exe_path] + args
        print(f"Running command: {' '.join(cmd)}")
        # self.logger.info(f"Running: {' '.join(cmd)}")
        try:
            result = subprocess.run(
                cmd,
                capture_output=capture_output,
                check=check,
                text=True,
                **kwargs
            )
            print(f"stdout: {result.stdout}")
            # self.logger.info(f"stdout: {result.stdout}")
            if result.stderr:
                print(f"stderr: {result.stderr}")
                # self.logger.error(f"stderr: {result.stderr}")
            return result
        except subprocess.CalledProcessError as e:
            print(f"Error executing {self.exe_path}: {e}")
            # self.logger.error(f"Execution failed: {e}")
            #raise

# Classes específicas para cada .exe
class SpatialiteXmlValidator(SpatialiteBase):
    """
    Inicializa a classe para spatialite_xml_validator.exe
    """
    def __init__(self):
        super().__init__("spatialite_xml_validator.exe")

    def help(self):
        """
        Exibe a ajuda do executável.
        """
        print("""
        usage: spatialite_xml_validate -f xml-path
        or: spatialite_xml_validate -l list-of-paths-file
        """)

class SpatialiteXmlPrint(SpatialiteBase):
    """
    Inicializa a classe para spatialite_xml_print.exe
    """
    def __init__(self):
        super().__init__("spatialite_xml_print.exe")

    def help(self):
        """
        Exibe a ajuda do executável.
        """
        print("""
        usage: spatialite_xml_printf ARGLIST
        ==============================================================
        -h or --help                    print this help message
        -v or --version                 print version infos
        -d or --db-path     pathname    the SpatiaLite DB [INPUT] path

        -x or --xml-path    pathname    the XML file [OUTPUT] path
        -cs or --cache-size    num      DB cache size (how many pages)
        -m or --in-memory               using IN-MEMORY database
        """)

class SpatialiteXmlLoad(SpatialiteBase):
    """
    Inicializa a classe para spatialite_xml_load.exe
    """
    def __init__(self):
        super().__init__("spatialite_xml_load.exe")

    def help(self):
        """
        Exibe a ajuda do executável.
        """
        print("""
        usage: spatialite_xml_load ARGLIST
        ==============================================================
        -h or --help                    print this help message
        -x or --xml-path pathname       the XML file path
        -d or --db-path     pathname    the SpatiaLite DB path

        you can specify the following options as well
        -cg or --collapsed-gml          collapsed GML Geometries
        -xl or --xlink-href             special GML xlink:href handling
        -nl or --nl-level      num      tree-level for table-names (dft: 0)
        -pl or --parent-levels num      how many ancestors for table-names (dft: -1)
        -jo or --journal-off            unsafe [but faster] mode
        -cs or --cache-size    num      DB cache size (how many pages)
        -m or --in-memory               using IN-MEMORY database
        """)
        
class SpatialiteXmlCollapse(SpatialiteBase):
    """
    Inicializa a classe para spatialite_xml_collapse.exe
    """
    def __init__(self):
        super().__init__("spatialite_xml_collapse.exe")

    def help(self):
        """
        Exibe a ajuda do executável.
        """
        print("""
        usage: spatialite_xml_collapse ARGLIST
        ==============================================================
        -h or --help                    print this help message
        -v or --version                 print version infos
        -d or --db-path     pathname    the SpatiaLite DB path

        you can specify the following options as well
        -dd or --delete-duplicates      remove all duplicate rows except one
        -nl or --nl-level      num      tree-level for table-names (dft: 0)

        -jo or --journal-off            unsafe [but faster] mode
        -cs or --cache-size    num      DB cache size (how many pages)
        -m or --in-memory               using IN-MEMORY database
        """)

class SpatialiteXml2Utf8(SpatialiteBase):
    """
    Inicializa a classe para spatialite_xml2utf8.exe
    """
    def __init__(self):
        super().__init__("spatialite_xml2utf8.exe")

    def help(self):
        """
        Exibe a ajuda do executável.
        """
        print("""
        usage: spatialite_utf8 input-charset <input >output
        """)

class SpatialiteTool(SpatialiteBase):
    """
    Inicializa a classe para spatialite_tool.exe
    """
    def __init__(self):
        super().__init__("spatialite_tool.exe")

    def help(self):
        """
        Exibe a ajuda do executável.
        """
        print("""
        usage: spatitalite_tool CMD ARGLIST
        ==============================================================
        CMD has to be one of the followings:
        ------------------------------------
        -h or --help                      print this help message
        -v or --version                   print version infos
        -i or --import                    import [CSV/TXT, DBF or SHP]
        -e or --export-shp                exporting some shapefile

        supported ARGs are:
        -------------------
        -dbf or --dbf-path pathname       the full DBF path
        -shp or --shapefile pathname      the shapefile path [NO SUFFIX]
        -d or --db-path pathname          the SpatiaLite db path
        -t or --table table_name          the db geotable
        -g or --geometry-column col_name  the Geometry column
        -c or --charset charset_name      a charset name
        -s or --srid SRID                 the SRID
        --type         [POINT | LINESTRING | POLYGON | MULTIPOINT]

        optional ARGs for SHP import are:
        ---------------------------------
        -2 or --coerce-2d                  coerce to 2D geoms [x,y]
        -k or --compressed                 apply geometry compression

        examples:
        ---------
        spatialite_tool -i -dbf abc.dbf -d db.sqlite -t tbl -c CP1252
        spatialite_tool -i -shp abc -d db.sqlite -t tbl -c CP1252 [-s 4326] [-g geom]
        spatialite_tool -i -shp abc -d db.sqlite -t tbl -c CP1252 [-s 4326] [-2] [-k]
        spatialite_tool -e -shp abc -d db.sqlite -t tbl -g geom -c CP1252 [--type POINT]
        """)

class SpatialiteOsmRaw(SpatialiteBase):
    """
    Inicializa a classe para spatialite_osm_raw.exe
    """
    def __init__(self):
        super().__init__("spatialite_osm_raw.exe")

    def help(self):
        """
        Exibe a ajuda do executável.
        """
        print("""
        usage: spatialite_osm_raw ARGLIST
        ==============================================================
        -h or --help                    print this help message
        -v or --version                 print version infos
        -o or --osm-path pathname       the OSM-file path
                        both OSM-XML (*.osm) and OSM-ProtoBuf
                        (*.osm.pbf) are indifferently supported.

        -d or --db-path  pathname       the SpatiaLite DB path

        you can specify the following options as well
        -cs or --cache-size    num      DB cache size (how many pages)
        -m or --in-memory               using IN-MEMORY database
        -jo or --journal-off            unsafe [but faster] mode
        """)

class SpatialiteOsmOverpass(SpatialiteBase):
    """
    Inicializa a classe para spatialite_osm_overpass.exe
    """
    def __init__(self):
        super().__init__("spatialite_osm_overpass.exe")

    def help(self):
        """
        Exibe a ajuda do executável.
        """
        print("""
        usage: spatialite_osm_overpass ARGLIST
        ==============================================================
        -h or --help                    print this help message
        -v or --version                 print version infos
        -d or --db-path     pathname    the SpatiaLite DB path
        -minx or --bbox-minx  coord     BoundingBox - west longitude
        -maxx or --bbox-maxx  coord     BoundingBox - east longitude
        -miny or --bbox-miny  coord     BoundingBox - south latitude
        -maxy or --bbox-maxy  coord     BoundingBox - north latitude

        you can specify the following options as well
        -o or --osm-service   URL       URL of OSM Overpass service:
                                        http://overpass-api.de/api (default)
                                        http://overpass.osm.rambler.ru/cgi
                                        http://api.openstreetmap.fr/oapi
        -mode or --mode       mode      one of: RAW / MAP (default) / ROAD / RAIL
        -cs or --cache-size   num       DB cache size (how many pages)
        -m or --in-memory               using IN-MEMORY database
        -jo or --journal-off            unsafe [but faster] mode
        -p or --preserve                skipping final cleanup (preserving OSM tables)
        """)

class SpatialiteOsmNet(SpatialiteBase):
    """
    Inicializa a classe para spatialite_osm_net.exe
    """
    def __init__(self):
        super().__init__("spatialite_osm_net.exe")

    def help(self):
        """
        Exibe a ajuda do executável.
        """
        print("""
        usage: spatialite_osm_net ARGLIST
        ==============================================================
        -h or --help                    print this help message
        -v or --version                 print version infos
        -o or --osm-path pathname       the OSM-XML file path
                        both OSM-XML (*.osm) and OSM-ProtoBuf
                        (*.osm.pbf) are indifferently supported.

        -d or --db-path  pathname       the SpatiaLite DB path
        -T or --table    table_name     the db table to be fed

        you can specify the following options as well
        -cs or --cache-size    num      DB cache size (how many pages)
        -m or --in-memory               using IN-MEMORY database
        -jo or --journal-off            unsafe [but faster] mode
        -2 or --undirectional           double arcs

        --roads                         extract roads [default]
        --railways                      extract railways
                                        [mutually exclusive]

        template-file specific options:
        -ot or --out-template  path     creates a default template-file
        -tf or --template-file path     using a template-file
        """)

class SpatialiteOsmMap(SpatialiteBase):
    """
    Inicializa a classe para spatialite_osm_map.exe
    """
    def __init__(self):
        super().__init__("spatialite_osm_map.exe")

    def help(self):
        """
        Exibe a ajuda do executável.
        """
        print("""
        usage: spatialite_osm_map ARGLIST
        ==============================================================
        -h or --help                    print this help message
        -v or --version                 print version infos
        -o or --osm-path pathname       the OSM-XML file path
                        both OSM-XML (*.osm) and OSM-ProtoBuf
                        (*.osm.pbf) are indifferently supported.

        -d or --db-path  pathname       the SpatiaLite DB path

        you can specify the following options as well
        -cs or --cache-size    num      DB cache size (how many pages)
        -m or --in-memory               using IN-MEMORY database
        -n or --no-spatial-index        suppress R*Trees generation
        -jo or --journal-off            unsafe [but faster] mode
        """)

class SpatialiteOsmFilter(SpatialiteBase):
    """
    Inicializa a classe para spatialite_osm_filter.exe
    """
    def __init__(self):
        super().__init__("spatialite_osm_filter.exe")

    def help(self):
        """
        Exibe a ajuda do executável.
        """
        print("""
        usage: spatialite_osm_filter ARGLIST
        ==============================================================
        -h or --help                    print this help message
        -v or --version                 print version infos
        -o or --osm-path pathname       the OSM-XML [output] file path
        -w or --wkt-mask-path pathname  path of text file [WKT mask]
        -d or --db-path  pathname       the SpatiaLite DB path

        you can specify the following options as well
        -cs or --cache-size    num      DB cache size (how many pages)
        -m or --in-memory               using IN-MEMORY database
        -jo or --journal-off            unsafe [but faster] mode
        """)

class SpatialiteNetwork(SpatialiteBase):
    """
    Inicializa a classe para spatialite_network.exe
    """
    def __init__(self):
        super().__init__("spatialite_network.exe")

    def help(self):
        """
        Exibe a ajuda do executável.
        """
        print("""
        usage: spatialite_network ARGLIST
        ==============================================================
        -h or --help                      print this help message
        -v or --version                   print version infos
        -d or --db-path pathname          the SpatiaLite db path
        -T or --table table_name          the db table to be validated
        -f or --from-column col_name      the column for FromNode
        -t or --to-column col_name        the column for ToNode
        -g or --geometry-column col_name  the column for Geometry
        -c or --cost-column col_name      the column for Cost
                                        if omitted, GLength(g)
                                        will be used by default

        you can specify the following options as well:
        ----------------------------------------------
        --a-star-supported                *default*
        --a-star-excluded
        -n or --name-column col_name      the column for RoadName
        --bidirectional                   *default*
        --unidirectional

        if *bidirectional* each arc connecting FromNode to ToNode is
        implicitly connecting ToNode to FromNode as well; in this case
        you can select the following further options:
        --oneway-tofrom col_name
        --oneway-fromto col_name
        both columns are expected to contain BOOLEAN values [1-0];
        1 means that the arc connection in the given direction is
        valid, otherwise 0 means a forbidden connection

        in order to create a permanent NETWORK-DATA table
        you can select the following options:
        -o or --output-table table_name
        -vt or --virtual-table table_name
        --overwrite-output
        """)

class SpatialiteGml(SpatialiteBase):
    """
    Inicializa a classe para spatialite_gml.exe
    """
    def __init__(self):
        super().__init__("spatialite_gml.exe")

    def help(self):
        """
        Exibe a ajuda do executável.
        """
        print("""
        usage: spatialite_gml ARGLIST
        ==============================================================
        -h or --help                    print this help message
        -v or --version                 print version infos
        -g or --gml-path pathname       the GML-XML file path
        -d or --db-path     pathname    the SpatiaLite DB path

        -t or --table-name  name        the DB table name

        you can specify the following options as well
        -m or --in-memory               using IN-MEMORY database
        -n or --no-spatial-index        suppress R*Tree generation
        """)

class SpatialiteDxf(SpatialiteBase):
    """
    Inicializa a classe para spatialite_dxf.exe
    """
    def __init__(self):
        super().__init__("spatialite_dxf.exe")

    def help(self):
        """
        Exibe a ajuda do executável.
        """
        print("""
        usage: spatialite_dxf ARGLIST
        ==============================================================
        -h or --help                    print this help message
        -v or --version                 print version infos
        -d or --db-path  pathname       the SpatiaLite DB path
        -x or --dxf-path pathname       the input DXF path

        you can specify the following options as well:
        ----------------------------------------------
        -s or --srid       num          an explicit SRID value
        -p or --prefix  layer_prefix    prefix for DB layer names
        -l or --layer   layer_name      will import a single DXF layer
        -all or --all-layers            will import all layers (default)

        -distinct or --distinct-layers  respecting individual DXF layers
        -mixed or --mixed-layers        merging layers altogether by type
                                        distinct|mixed are mutually
                                        exclusive; by default: distinct

        -auto or --auto_2d_3d           2D/3D based on input geometries
        -2d or --force_2d               unconditionally force 2D
        -3d or --force_3d               unconditionally force 3D
                                        auto|2d|3d are mutually exclusive
                                        by default: auto

        -linked or --linked-rings      support linked polygon rings
        -unlinked or --unlinked-rings  support unlinked polygon rings
                                    linked|unlinked are mutually exclusive
                                        by default: none

        -a or --append                 appends to already exixting tables

        --------------------------
        -m or --in-memory               using IN-MEMORY database
        -jo or --journal-off            unsafe [but faster] mode
        """)

class SpatialiteDem(SpatialiteBase):
    """
    Inicializa a classe para spatialite_dem.exe
    """
    def __init__(self):
        super().__init__("spatialite_dem.exe")

    def help(self):
        """
        Exibe a ajuda do executável.
        """
        print("""
        usage: spatialite_dem ARGLIST
        ==============================================================
        -h or --help                    print this help message
        ========================== Parameters ========================
        -- -- ---------------- Dem-Data Database ---------------- --
        -ddem or --dem-path  pathname to the SpatiaLite Dem DB
        -tdem or --table-dem table_name [SpatialTable or SpatialView]
        -gdem or --geometry-dem-column col_name the Geometry column
                must be a POINT Z or a POINT ZM type
        -rdem or --dem-resolution of the dem points while searching
                the automatic resolution calculation is based on the row_count
                within the extent, which may not be correct!
                Use '-rdem' to set a realistic value

        -- -- -------------- Source-Update-Database ----------------- --
        -d or --db-path pathname to the SpatiaLite DB
        -t or --table table_name,  must be a SpatialTable
        -g or --geometry-column the Geometry column to update
                must  be a Z or a ZM Dimension type
                use CastToXYZ(geom) or CastToXYZM(geom) to convert
        -- -- --------------- General Parameters ---------------- --
        -mdem or --copy-m [0=no, 1= yes [default] if exists]
        -default_srid or --srid for use with -fetchz
        -fetchz_xy x- and y-value for use with -fetchz
        -v or  --verbose messages during -updatez and -fetchz
        -save_conf based on active -ddem , -tdem, -gdem and -srid when valid

        -- -- -------------------- Notes:  ---------------------- --
        -I-> the Z value will be copied from the nearest point found
        -I-> the Srid of the source Geometry and the Dem-POINT can be different
        -I-> when -fetchz_xy is used in a bash script, -v should not be used
                the z-value will then be returned as the result

        -- -- -------------------- Conf file:  ------------------- --
        -I-> if 'SPATIALITE_DEM' is set with the path to a file
        -I--> 'export SPATIALITE_DEM=/long/path/to/file/berlin_dhh92.conf'
        -I-> then '-save_conf' save the config to that file
        -I-> this file will be read on each application start, setting those values
        -I--> the parameters for :
                which Dem-Database and Geometry and the default_srid to use for queries
                -> would then not be needed

        -- -- ---------------- Importing .xyz files:  ------------------- --
        -I-> a single xyz.file or a directory containing .xyz files can be given
                for directories: only files with the extension .xyz will be searched for
        -I-> a single list.file inside a directory containing .xyz files can be given
                each line containing the file-name that must exist in that directory
        -I-> validty checks are done before importing xyz-files
                the first line may contain only 3 double values (point_x/y/z)
                if valid, the file-name and the point_x/y points are stored
                when importing, the list will be read based of the y/x points

        -- -- ---------------- Sorting .xyz files:  ---------------------- --
        -I->  xyz.files should be sorted:
                y='South to North' and x='West to East':
                sort -n -k2 -k1 input_file.xyz -o output_file.sort.xyz
        =========================== Commands ===========================
        -sniff   [default] analyse settings without UPDATE of z-values
        -updatez Perform UPDATE of z-values
        -fetchz Perform Query of z-values using  -fetchz_x_y and default_srid
                will be assumed when using  -fetchz_x_y
        -create_dem create Dem-Database using -ddem,-tdem, -gdem and -srid for the Database
                -d as a dem.xyz file
        -import_xyz import another .xyz file into a Dem-Database created with -create_dem
                these points will not be sorted, but added to the end
        =========================== Sample ===========================
        --> with 'SPATIALITE_DEM' set:
        spatialite_dem -fetchz_xy  24700.55278283251 20674.74537357586
        33.5600000
        ==============================================================
        """)

class SpatialiteConvert(SpatialiteBase):
    """
    Inicializa a classe para spatialite_convert.exe
    """
    def __init__(self):
        super().__init__("spatialite_convert.exe")

    def help(self):
        """
        Exibe a ajuda do executável.
        """
        print("""
        usage: spatialite_convert ARGLIST
        ==============================================================
        -h or --help                    print this help message
        -v or --version                 print version infos
        -d or --db-path  pathname       the SpatiaLite DB path

        -tv or --target-version  num    target Version (2, 3, 4, 5)
        """)

class Spatialite(SpatialiteBase):
    """
    Inicializa a classe para spatialite.exe
    """
    def __init__(self):
        super().__init__("spatialite.exe")

    def help(self):
        """
        Exibe a ajuda do executável.
        """
        print("""
        Usage: spatialite.exe [OPTIONS] FILENAME [SQL]
        FILENAME is the name of an SQLite database. A new database is created
        if the file does not previously exist.
        OPTIONS include:
        -bail                stop after hitting an error
        -batch               force batch I/O
        -column              set output mode to 'column'
        -cmd command         run "command" before reading stdin
        -csv                 set output mode to 'csv'
        -echo                print commands before execution
        -init filename       read/process named file
        -[no]header          turn headers on or off
        -help                show this message
        -html                set output mode to HTML
        -interactive         force interactive I/O
        -line                set output mode to 'line'
        -list                set output mode to 'list'
        -silent              suppress the welcome message
        -nullvalue 'text'    set text string for NULL values
        -separator 'x'       set output field separator (|)
        -stats               print memory stats before each finalize
        -version             show SQLite version
        -vfs NAME            use NAME as the default VFS
        """)

class ShpSanitize(SpatialiteBase):
    """
    Inicializa a classe para shp_sanitize.exe
    """
    def __init__(self):
        super().__init__("shp_sanitize.exe")

    def help(self):
        """
        Exibe a ajuda do executável.
        """
        print("""
        usage: shp_sanitize ARGLIST
        =================================================================
        -h or --help                      print this help message
        -v or --version                   print version infos
        -idir or --in-dir   dir-path      directory expected to contain
                                        all SHP to be checked
        -odir or --out-dir  dir-path      <optional> directory where to
                                        store all repaired SHPs

        ======================= optional args ===========================
        -geom or --invalid-geoms          checks for invalid Geometries
        -esri or --esri-flag              tolerates ESRI-like inner holes
        -force or --force-repair          unconditionally repair
        """)

class ShpDoctor(SpatialiteBase):
    """
    Inicializa a classe para shp_doctor.exe
    """
    def __init__(self):
        super().__init__("shp_doctor.exe")

    def help(self):
        """
        Exibe a ajuda do executável.
        """
        print("""
        usage: shp_doctor ARGLIST
        ==============================================================
        -h or --help                      print this help message
        -v or --version                   print version infos
        -i or --in-path pathname          the SHP path [no suffix]
                                                    or
                                        the full DBF path [-dbf]

        you can specify the following options as well
        --analyze                 *default*
        --ignore-shape-type       ignore entities' shape-type
        --ignore-extent           ignore coord consistency
        --ignore-shx              ignore the SHX file
        -dbf or --bare-dbf        bare DBF check
        """)

class ExifLoader(SpatialiteBase):
    """
    Inicializa a classe para exif_loader.exe
    """
    def __init__(self):
        super().__init__("exif_loader.exe")

    def help(self):
        """
        Exibe a ajuda do executável.
        """
        print("""
        usage: exif_loader ARGLIST
        ==============================================================
        -h or --help                    print this help message
        -v or --version                 print version infos
        -d or --db-path    pathname     the SpatiaLite db path
        -D or --dir        dir_path     the DIR path containing EXIF files
        -f or --file-path  file_name    a single EXIF file

        you can specify the following options as well
        --any-exif         *default*
        --gps-exif-only

        --metadata         *default*
        --no-metadata
        """)

# Exemplos de uso das classes Spatialite:

# from modules.osmtools.spatialite import SpatialiteXmlValidator, Spatialite, ShpSanitize

# # Exemplo 1: Validar um arquivo XML
# validator = SpatialiteXmlValidator()
# result = validator.run(["input.xml"])  # Substitua por argumentos reais
# print(result.stdout)

# # Exemplo 2: Executar o spatialite principal
# spatialite = Spatialite()
# result = spatialite.run(["--help"])  # Exibe ajuda do executável
# print(result.stdout)

# # Exemplo 3: Usar outro executável, como ShpSanitize
# shp_sanitize = ShpSanitize()
# result = shp_sanitize.run(["input.shp"])  # Substitua por argumentos reais
# print(result.stdout)
