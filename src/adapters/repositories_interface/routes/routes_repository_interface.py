from abc import ABC, abstractmethod
import json
import pandas as pd

class IRoutesRepository(ABC):

    @abstractmethod    
    def get_route(self, lat_init, log_init, lat_fim, log_fim) -> pd.DataFrame:
        '''Retorna uma rota'''