from typing import Optional
import psycopg2 # type: ignore
import sqlite3
import os

from src.infra.db.interfaces.connection_interface import IDBConnectionHandler
from src.infra.config import configSQlite
from src.infra.config import configPG 
from src.infra.config import mod_spatialite
from src.infra.config.api_config import api_config



class PGconnectionHandler(IDBConnectionHandler):
    def __init__(self) -> None:
        self.__conn_pg = None
        self.__config_pg = {
            "database": configPG["database"],
            "user": configPG["user"],
            "host": configPG["host"],
            "password": configPG["password"],
            "port": configPG["port"],
        }

    def __create_conn_pg(self) -> Optional[psycopg2.extensions.connection]:
        '''Criando conexão com o Postgre'''
        try:
            self.__conn_pg = psycopg2.connect(**self.__config_pg)
            return self.__conn_pg
        except Exception as e:
            print(f"Error connecting to PostgreSQL: {e}")
            return None

    def get_conn(self) -> Optional[psycopg2.extensions.connection]:
        if self.__conn_pg is None:
            return self.__create_conn_pg()
        return self.__conn_pg
    
    def __enter__(self)-> Optional[psycopg2.extensions.connection]:
        return self.get_conn()

    def __exit__(self, exc_type, exc_value, exc_tb):
        if self.__conn_pg:
            self.__conn_pg.close()
            self.__conn_pg = None


class SQliteConnectionHandler:
    def __init__(self, db_path) -> Optional[sqlite3.Connection]:
        self.__conn_sqlite: Optional[sqlite3.Connection] = None
        self.db_path = db_path 
        self.mod_path = mod_spatialite["mod_spatialite_path"]
        self.flag_exec_windows = False

        if api_config["execute_windows"] in ("True", "true", True):
            self.flag_exec_windows = True 
            
        self.path_init = os.getcwd()


    def __create_conn_sqlite(self) -> Optional[sqlite3.Connection]:
        """Cria conexão com o banco SQLite."""
        try:
            self.__conn_sqlite = sqlite3.connect(
                self.db_path,
                check_same_thread=False
            )
            self.__conn_sqlite.enable_load_extension(True)



            if self.flag_exec_windows:
                print("EXECUTANDO API NO: WINDOWS")
                os.chdir(self.mod_path)
                self.__conn_sqlite.load_extension(f'{self.mod_path}/mod_spatialite.dll')
                self.__conn_sqlite.execute('SELECT load_extension("mod_spatialite.dll")')
                os.chdir(self.path_init)
            else:
                print("EXECUTANDO API NO: LINUX")
                self.__conn_sqlite.load_extension(f'{self.mod_path}/mod_spatialite.so')
                self.__conn_sqlite.execute('SELECT load_extension("mod_spatialite.so")')

            #Isso é preciso se acaso necessário usar conversor de SRDI
            #path_proj= r'src\infra\db\settings\proj.db'
            #query_proj = f"SELECT PROJ_SetDatabasePath('{path_proj}');"
            #self.__conn_sqlite.execute(query_proj)

            return self.__conn_sqlite
        
        except Exception as e:
            print(f"Erro ao conectar ao SQLite: {e}")
            return None

    def get_conn(self) -> Optional[sqlite3.Connection]:
        if self.__conn_sqlite is None:
            return self.__create_conn_sqlite()
        return self.__conn_sqlite

    def __enter__(self) -> Optional[sqlite3.Connection]:
        return self.get_conn()

    def __exit__(self, exc_type, exc_value, exc_tb):
        if self.__conn_sqlite:
            self.__conn_sqlite.close()
            self.__conn_sqlite = None

