import pandas as pd #type: ignore
import logging

from src.infra.db.interfaces.connection_repository_interface import IDatabaseRepository
from src.infra.db.settings.connection import SQliteConnectionHandler
from src.infra.config import configSQlite

class DatabaseRepository(IDatabaseRepository):
    
    @classmethod
    def run_query(cls, db_handler, query: str, will_return: bool = False):
        try:
            with db_handler as conn:
                if will_return:
                    cursor = conn.cursor()
                    cursor.execute(query)
                    rows = cursor.fetchall()
                    columns = [desc[0] for desc in cursor.description]
                    df = pd.DataFrame(rows, columns=columns)
                    return df
                else:
                    cursor = conn.cursor()
                    cursor.execute(query)
                    conn.commit()
                    return True
                
        except Exception as e:
            print(str(e))
            print(f'Erro ao executar a query: {query}\'')
            return False
        
    def get_connection_db_routes(self):
        try:
            db_conection = SQliteConnectionHandler(configSQlite["path_database"])
            return db_conection
        except Exception as e:
            print(str(e))
            print("ERRO AO OBTER CONEXAO")

    def get_connection_db_locales(self):
        try:
            db_conection = SQliteConnectionHandler(configSQlite["path_database_locales"])
            return db_conection
        except Exception as e:
            print(str(e))
            print("ERRO AO OBTER CONEXAO")