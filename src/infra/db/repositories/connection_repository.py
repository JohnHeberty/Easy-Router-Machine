import pandas as pd #type: ignore
import logging

from src.infra.db.settings.connection import SQliteConnectionHandler
from src.infra.db.interfaces.connection_repository_interface import IDatabaseRepository

class DatabaseRepository(IDatabaseRepository):
    
    @classmethod
    def run_query(cls, query: str, will_return: bool = False):
        try:
            db_handler = SQliteConnectionHandler()

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
            print(f'Erro ao executar a query: {query}\'')
            return False