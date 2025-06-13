import pandas as pd #type: ignore
import logging

from src.infra.db.settings.connection import PGconnectionHandler
from src.infra.db.interfaces.connection_repository_interface import IDatabaseRepository

class DatabaseRepository(IDatabaseRepository):
    
    
    @classmethod
    def run_query(cls, query: str, dados: list = None, will_return: bool = False):
        try:
            # db_handler = PGconnectionHandler()
            # with db_handler as conn:
            #     if will_return:
            #         df = pd.read_sql(query, conn, params=dados)
            #         conn.commit()
            #         return df
            #     else:
            #         cursor = conn.cursor()
            #         cursor.execute(query, dados)
            #         conn.commit()
            #         return True
            
            return "TESTE"

        except Exception as e:
            print(f'Erro ao executar a query: {query}\nCom argumentos: {dados}\nErro: {e}')
            return False