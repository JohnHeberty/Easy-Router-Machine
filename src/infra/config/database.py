import os
from dotenv import load_dotenv

load_dotenv()


configPG = {
    "database"  : 1,
    "user"      : 1,
    "host"      : 1,
    "password"  : 1,
    "port"      : 1,
}

configSQlite = {
    "path_database"  : os.getenv("PATH_DATABASE_SQLITE"),
}

mod_spatialite = {
    "mod_spatialite_path"  : os.getenv("PATH_MOD_SPATIALITE"),
}
