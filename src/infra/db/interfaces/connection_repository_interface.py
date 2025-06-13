from abc import abstractmethod, ABC
from typing import Optional
import pandas as pd #type: ignore 

class IDatabaseRepository(ABC):
    @classmethod
    def run_query(cls, query: str, will_return: bool)-> Optional[pd.DataFrame]:
        '''
        Executa consultas no banco \n
        Pode retornar um Dataframe ou None
        '''