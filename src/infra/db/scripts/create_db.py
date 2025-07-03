import os
import sqlite3
from src.infra.db.scripts.templates_db import table_infraestrutura_rodoviaria
from src.infra.db.settings.connection import SQliteConnectionHandler
from src.infra.config import configSQlite

class DatabaseInitializer:
    def __init__(self):
        self.db_path = configSQlite["path_database_locales"]

        if not self.db_path.endswith("db_locales.sqlite"):
            raise ValueError("O nome do arquivo do path deve ser 'db_locales.sqlite'")


    def create_db_locales(self):
        try:
            if not os.path.exists(self.db_path):
                self.conn = SQliteConnectionHandler(self.db_path).get_conn()
                print("Criando banco de dados de localização...")
                cursor = self.conn.cursor()
                cursor.executescript(table_infraestrutura_rodoviaria)
                self.conn.commit()
                print("Banco locales criado com sucesso.")
            else:
                #print("Banco db_locales.sqlite já existe.")
                pass
        except sqlite3.OperationalError as e:
            print(f"Erro operacional do SQLite: {e}")
        except Exception as e:
            print(f"Erro inesperado ao criar o banco: {e}")
