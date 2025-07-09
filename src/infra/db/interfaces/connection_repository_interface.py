from abc import abstractmethod, ABC
from typing import Optional
import pandas as pd #type: ignore 
from sqlite3 import Connection

class IDatabaseRepository(ABC):
    @classmethod
    def run_query(cls, db_handler, query: str, will_return: bool)-> Optional[pd.DataFrame]:
        '''
        Executa consultas no banco \n
        Pode retornar um Dataframe ou None
        '''
    def get_connection_db_routes(self) -> Optional[Connection]:
        '''
        Obtem a conexao do banco de dados do banco de rotas
        '''
        
